"""
Plugin : plugin_llm_fallback
Rôle : Fournir une réponse de secours via un modèle par défaut si les autres ont échoué
Version : 1.1
Auteur : Toi & GPT
"""

import logging
import httpx
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_fallback")

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
FALLBACK_MODEL = "mistral"

class PluginLLMFallback(BasePlugin):
    meta = Meta(
        name="plugin_llm_fallback",
        version="1.1",
        priority=3.6,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("llm_prompt", "").strip()
        response = ctx.get("response", "").strip()

        if response:
            ctx.setdefault("plugins_log", []).append("plugin_llm_fallback : réponse déjà présente → skip.")
            return ctx

        if not prompt:
            ctx.setdefault("plugins_log", []).append("plugin_llm_fallback : prompt absent → abort.")
            return ctx

        ctx.setdefault("plugins_log", []).append(f"plugin_llm_fallback : fallback activé via {FALLBACK_MODEL}")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                r = await client.post(
                    OLLAMA_ENDPOINT,
                    json={
                        "model": FALLBACK_MODEL,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                r.raise_for_status()
                data = r.json()
                fallback_response = data.get("response", "").strip()

                if fallback_response:
                    ctx["response"] = fallback_response
                    ctx.setdefault("plugins_log", []).append(
                        f"plugin_llm_fallback : réponse obtenue via {FALLBACK_MODEL} ({len(fallback_response)} chars)"
                    )
                else:
                    ctx.setdefault("plugins_log", []).append(
                        f"plugin_llm_fallback : {FALLBACK_MODEL} a répondu vide."
                    )
        except Exception as e:
            err = f"plugin_llm_fallback : exception → {str(e)}"
            ctx.setdefault("plugins_log", []).append(err)
            logger.error(err)

        return ctx
