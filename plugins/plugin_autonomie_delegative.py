"""
Plugin : autonomie_delegative
Rôle : Suggérer automatiquement de déléguer certaines tâches à une instance fille ou une API externe
Priorité : 2.8 (après analyse de tâche, avant décision)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autonomie_delegative")

class AutonomieDelegativePlugin(BasePlugin):
    meta = Meta(
        name="autonomie_delegative",
        priority=2.8,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTS_CLES_DELEGABLES = [
        "télécharger", "traiter un fichier", "résumer un document", "convertir", "surveiller", "régénérer", "répéter"
    ]

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        plugins_log = ctx.setdefault("plugins_log", [])
        suggestions = ctx.setdefault("delegations_proposees", [])

        for mot in self.MOTS_CLES_DELEGABLES:
            if mot in message:
                suggestion = f"Souhaites-tu que je délègue cette tâche à une AGI fille ou à un module externe ? ({mot})"
                suggestions.append(suggestion)
                plugins_log.append(f"AutonomieDelegativePlugin : suggestion de délégation → {mot}")
                logger.info(f"[autonomie_delegative] Suggestion d’AGI fille pour : {mot}")
                break

        return ctx
