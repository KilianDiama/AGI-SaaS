# plugins/plugin_utilisation_competence.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.utilisation_competence")

class PluginUtilisationCompetence(BasePlugin):
    meta = Meta(
        name="plugin_utilisation_competence",
        version="1.0",
        priority=4.6,
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_utilisation_competence"

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        competences = ctx.get("competences_mémorisées", {})

        if not objectif or not competences:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun objectif clair ou aucune compétence mémorisée.")
            return ctx

        utilisées = ctx.setdefault("competences_utilisees", [])

        for objet, blocs in competences.items():
            if objet.lower() in objectif:
                utilisées.extend(blocs)
                logger.info(f"[{self.nom}] Compétence activée pour : {objet}")

        ctx.setdefault("plugins_log", []).append(
            f"{self.nom} : {len(utilisées)} blocs de compétences activés"
        )
        return ctx
