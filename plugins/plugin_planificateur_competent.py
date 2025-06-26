# plugins/plugin_planificateur_competent.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.planificateur_competent")

class PluginPlanificateurCompetent(BasePlugin):
    meta = Meta(
        name="plugin_planificateur_competent",
        version="1.0",
        priority=4.8,
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_planificateur_competent"

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        blocs = ctx.get("competences_utilisees", [])

        if not objectif or not blocs:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun plan généré (pas d’objectif ou de compétence activée).")
            return ctx

        plan = []
        for bloc in blocs:
            titre = bloc.get("titre") or bloc.get("objet", "étape")
            if titre.lower() not in objectif:
                plan.append(f"Appliquer : {titre}")

        if plan:
            ctx["plan_generé"] = plan
            logger.info(f"[{self.nom}] Plan généré à partir des compétences : {plan}")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : {len(plan)} étapes planifiées")
        else:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : toutes les compétences semblaient déjà incluses.")

        return ctx
