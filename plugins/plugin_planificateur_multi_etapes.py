"""
Plugin : planificateur_multi_etapes
Rôle : Décomposer automatiquement une tâche complexe en plusieurs sous-étapes claires
Priorité : 2.2 (avant simulation ou décision)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.planificateur_multi_etapes")

class PlanificateurMultiEtapesPlugin(BasePlugin):
    meta = Meta(
        name="planificateur_multi_etapes",
        priority=2.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTS_COMPLEXITE = ["plan", "organise", "long", "projet", "tâche", "dossier", "analyse", "objectifs", "phases"]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()
        plan_en_cours = ctx.get("plan_en_cours")

        # Déjà un plan en cours → pas besoin de recalcul
        if plan_en_cours:
            return ctx

        if any(mot in message for mot in self.MOTS_COMPLEXITE):
            # Exemples de détection et proposition de découpe simple (LLM plus tard)
            ctx["plan_en_cours"] = [
                "1. Comprendre la demande",
                "2. Identifier les éléments nécessaires",
                "3. Structurer la réponse",
                "4. Proposer une solution claire",
                "5. Vérifier la cohérence"
            ]
            plugins_log.append("PlanificateurMultiEtapesPlugin : plan généré automatiquement")
            logger.info("[planificateur_multi_etapes] Planification déclenchée.")

        return ctx
