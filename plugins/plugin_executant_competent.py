# plugins/plugin_executant_competent.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.executant_competent")

class PluginExecutantCompetent(BasePlugin):
    meta = Meta(
        name="plugin_executant_competent",
        version="1.0",
        priority=4.9,
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_executant_competent"

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan_generé", [])
        index = ctx.get("etape_actuelle", 0)
        competences = ctx.get("competences_disponibles", {})

        if index >= len(plan):
            ctx["etat_execution"] = "terminé"
            logger.info(f"[{self.nom}] Toutes les étapes du plan ont été exécutées.")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : toutes les étapes terminées.")
            return ctx

        etape = plan[index]
        nom_competence = etape.replace("Appliquer : ", "").strip().lower()

        if nom_competence in competences:
            logger.info(f"[{self.nom}] Exécution de la compétence : {nom_competence}")
            try:
                ctx = await competences[nom_competence].run(ctx)
                ctx["etape_actuelle"] = index + 1
                ctx.setdefault("plugins_log", []).append(f"{self.nom} : étape exécutée → {etape}")
            except Exception as e:
                logger.error(f"[{self.nom}] Erreur durant exécution de '{nom_competence}' : {e}")
                ctx.setdefault("plugins_log", []).append(f"{self.nom} : erreur → {nom_competence} ❌")
        else:
            logger.warning(f"[{self.nom}] Compétence inconnue : {nom_competence}")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : compétence manquante → {nom_competence}")

        return ctx
