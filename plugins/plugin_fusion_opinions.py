"""
Plugin : fusion_opinions
Rôle : Fusionner plusieurs avis (AGI filles ou rôles cognitifs) en une réponse unifiée
Priorité : 4.2 (après débat, vote ou réponse multi-sources)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.fusion_opinions")

class FusionOpinionsPlugin(BasePlugin):
    meta = Meta(
        name="fusion_opinions",
        priority=4.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponses = ctx.get("llm_responses", [])

        if not reponses or len(reponses) < 2:
            return ctx  # rien à fusionner

        # Construction d'une synthèse simple
        synthese = "Synthèse des avis :\n\n"
        for rep in reponses:
            synthese += f"• {rep.strip()}\n"

        ctx["response"] = synthese.strip()
        ctx["llm_response"] = synthese.strip()
        plugins_log.append("FusionOpinionsPlugin : réponses multiples fusionnées intelligemment")
        logger.info(f"[fusion_opinions] {len(reponses)} opinions fusionnées.")

        return ctx
