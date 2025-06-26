"""
Plugin : fusion_reponses
Rôle : Fusionner la/les réponse(s) produite(s) par les plugins LLM locaux ou raisonneurs
Priorité : 4  (doit s’exécuter après les plugins llm_local* et llm_router)
Auteur : Matthieu & GPT
"""

import logging
from typing import List
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.fusion_reponses")

class FusionReponsesPlugin(BasePlugin):
    meta = Meta(
        name="fusion_reponses",
        priority=4.0,
        version="2.2",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        response_set = False

        def inject_response(text: str, label: str = None):
            final = f"{label} :\n{text.strip()}" if label else text.strip()
            ctx["response"] = final
            ctx["llm_response"] = text.strip()
            return final

        # 1. Vérifie s’il existe une réponse unique
        llm_response = ctx.get("llm_response")
        if isinstance(llm_response, str) and llm_response.strip():
            inject_response(llm_response)
            plugins_log.append("FusionReponsesPlugin : réponse ← llm_response (unique)")
            logger.info("[fusion_reponses] Réponse injectée depuis llm_response")
            return ctx

        # 2. Vérifie s’il existe plusieurs réponses (multi-modeles)
        llm_responses: List[str] = ctx.get("llm_responses", [])
        if isinstance(llm_responses, list):
            cleaned = [r.strip() for r in llm_responses if isinstance(r, str) and r.strip()]
            if cleaned:
                fusion = "\n\n".join(f"• {r}" for r in cleaned)
                inject_response(f"Fusion de {len(cleaned)} modèles :\n\n{fusion}")
                plugins_log.append(f"FusionReponsesPlugin : fusion de {len(cleaned)} réponses")
                logger.info(f"[fusion_reponses] {len(cleaned)} réponses fusionnées")
                return ctx

        # 3. Fallback : utilise d'autres clés secondaires
        fallbacks = [
            ("response_logique", "[Raisonnement logique]"),
            ("raisonneur_response", "[Synthèse raisonneur]"),
            ("analysis_feedback", "[Analyse AI]"),
            ("reflexion_interne", "[Réflexion AI]")
        ]

        for key, label in fallbacks:
            value = ctx.get(key)
            if isinstance(value, str) and value.strip():
                inject_response(value, label)
                plugins_log.append(f"FusionReponsesPlugin : fallback ← {key}")
                logger.warning(f"[fusion_reponses] Fallback utilisé depuis {key}")
                return ctx

        # 4. Aucun contenu détecté
        msg = "❌ Aucune réponse disponible depuis les LLM ou modules cognitifs."
        inject_response(msg)
        plugins_log.append("FusionReponsesPlugin : aucun contenu utilisable.")
        logger.error("[fusion_reponses] Échec critique : aucune réponse injectée")

        return ctx
