"""
Plugin : plugin_summary_fusion
Rôle : Résumer les réponses LLM de manière claire et condensée
Priorité : 3.9 (juste avant la réponse finale)
Auteur : Matt & GPT
"""

import logging
from typing import List, Optional  # ✅ Ajout de Optional
import httpx

from noyau_core import BasePlugin, Context, Meta  # ✅ Vérifie que ces imports sont bien valides dans ton projet

logger = logging.getLogger("plugin.summary_fusion")

OLLAMA_URL = "http://localhost:11434/api/generate"

class PluginSummaryFusion(BasePlugin):
    meta = Meta(
        name="plugin_summary_fusion",
        version="1.0",
        priority=3.9,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        responses: List[str] = ctx.get("llm_responses", [])
        if not responses:
            ctx["llm_summary"] = "[Aucune réponse à résumer]"
            ctx.setdefault("plugins_log", []).append("plugin_summary_fusion : aucune réponse à résumer")
            return ctx

        content = "\n\n".join(responses).strip()
        logger.info("[plugin_summary_fusion] Tentative de résumé...")

        summary = await self._try_llm_summary(content) or self._fallback_summary(content)

        ctx["llm_summary"] = summary
        ctx.setdefault("plugins_log", []).append("plugin_summary_fusion : résumé généré")
        return ctx

    async def _try_llm_summary(self, text: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json={
                        "model": "mistral",  # ✅ Assure-toi que le modèle 'mistral' est bien chargé dans Ollama
                        "prompt": f"Résume de façon claire, concise et lisible :\n\n{text}",
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                result = data.get("response", "").strip()
                if result:
                    logger.info("[plugin_summary_fusion] Résumé LLM généré.")
                    return result
        except Exception as e:
            logger.warning(f"[plugin_summary_fusion] Résumé LLM échoué : {e}")
        return None

    def _fallback_summary(self, text: str) -> str:
        lines = text.replace("\n", " ").split(". ")
        snippet = ". ".join(lines[:2]).strip()
        logger.info("[plugin_summary_fusion] Résumé de secours utilisé.")
        return snippet + "..." if snippet else "[Résumé indisponible]"
