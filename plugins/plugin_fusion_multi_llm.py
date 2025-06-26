# plugins/plugin_fusion_multi_llm.py

import logging
from noyau_core import BasePlugin, Context, Meta
import httpx

logger = logging.getLogger("plugin.fusion_multi_llm")

OLLAMA_URL = "http://localhost:11434/api/generate"

class FusionMultiLLMPlugin(BasePlugin):
    meta = Meta(
        name="fusion_multi_llm",
        priority=110,
        version="1.1",
        author="Toi & GPT"
    )

    async def call_ollama(self, prompt: str, model: str) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(OLLAMA_URL, json=payload)
                res.raise_for_status()
                return res.json().get("response", "")
        except Exception as e:
            logger.error(f"⚠️ Erreur avec le modèle {model} via Ollama : {e}")
            return f"[Erreur avec {model}]"

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("llm_prompt") or ctx.get("payload", {}).get("message", "")
        models = ctx.get("llm_models", [])
        backend = ctx.get("llm_backend", "ollama")

        if not prompt or not models:
            logger.warning("❌ Pas de prompt ou de modèles spécifiés.")
            ctx["response"] = "Aucune réponse possible (pas de prompt ou de modèles)."
            return ctx

        if backend != "ollama":
            logger.warning("🚫 Backend non supporté (seul 'ollama' est géré ici).")
            ctx["response"] = "Ce plugin ne gère que les backends locaux (ollama)."
            return ctx

        responses = []
        for model in models:
            logger.info(f"🤖 Appel de {model} via Ollama...")
            reply = await self.call_ollama(prompt, model)
            responses.append(f"[{model}] {reply.strip()}")

        ctx["llm_responses"] = responses
        fusion = "\n\n".join([f"🔹 {r}" for r in responses])
        ctx["response_llm"] = f"🤖 **Fusion des modèles ({len(models)})** :\n\n{fusion}"

        ctx.setdefault("plugins_log", []).append(
            f"FusionMultiLLMPlugin : {len(models)} réponses fusionnées."
        )
        return ctx
