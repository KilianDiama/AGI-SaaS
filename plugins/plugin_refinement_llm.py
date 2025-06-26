import logging
from noyau_core import BasePlugin, Context, Meta
import httpx

logger = logging.getLogger("plugin.refinement_llm")

REFINEMENT_MODEL_URL = "http://localhost:11434/api/generate"
REFINEMENT_MODEL_NAME = "llama3"  # ou mistral, selon préférences

class PluginRefinementLLM(BasePlugin):
    meta = Meta(
        name="plugin_refinement_llm",
        version="1.0",
        priority=4.8,  # Juste avant PluginResponseResolver
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        raw = ctx.get("response", "")
        style = ctx.get("style_instruction", "")
        if not raw or len(raw.strip()) < 10:
            logger.info("[refinement_llm] Pas de réponse à raffiner.")
            ctx.setdefault("plugins_log", []).append("plugin_refinement_llm : rien à raffiner")
            return ctx

        prompt = (
            f"{style}\n\n"
            "Réécris cette réponse pour qu'elle soit plus claire, persuasive, fluide et humaine. "
            "Structure-la avec des paragraphes si besoin. Conserve le fond mais améliore la forme.\n\n"
            f"---\n{raw.strip()}\n---"
        )

        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(REFINEMENT_MODEL_URL, json={
                    "model": REFINEMENT_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                })
                res.raise_for_status()
                data = res.json()
                improved = data.get("response", "").strip()
        except Exception as e:
            logger.warning(f"[refinement_llm] Échec du raffinement : {e}")
            ctx.setdefault("plugins_log", []).append("plugin_refinement_llm : échec appel LLM")
            return ctx

        if improved:
            ctx["response"] = improved
            ctx.setdefault("plugins_log", []).append("plugin_refinement_llm : réponse raffinée")
            logger.info("[refinement_llm] Réponse raffinée avec succès.")
        return ctx
