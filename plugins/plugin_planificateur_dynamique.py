# plugins/plugin_planificateur_dynamique.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.planificateur_dynamique")

class PluginPlanificateurDynamique(BasePlugin):
    meta = Meta(
        name="plugin_planificateur_dynamique",
        version="1.0",
        priority=2.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip().lower()
        plan_actuel = ctx.get("plan", [])

        if not objectif or objectif == "non défini":
            logger.warning("Objectif non défini, plan par défaut généré.")
            objectif = "objectif à clarifier"
            ctx.setdefault("plugins_log", []).append("PluginPlanificateurDynamique : objectif manquant, plan par défaut injecté.")

        if not plan_actuel:
            plan = self._plan_initial(objectif)
            ctx["plan"] = plan
            ctx.setdefault("plugins_log", []).append("PluginPlanificateurDynamique : plan initial généré.")
        else:
            plan = self._ajuster_plan(plan_actuel)
            ctx["plan"] = plan
            ctx.setdefault("plugins_log", []).append("PluginPlanificateurDynamique : plan ajusté selon état actuel.")

        ctx["plan_meta"] = {
            "plugin": self.meta.name,
            "objectif": objectif,
            "étapes_totales": len(plan)
        }

        return ctx

    def _plan_initial(self, objectif: str) -> list:
        return [
            {"étape": "Clarifier l’objectif", "status": "à faire"},
            {"étape": "Identifier les composants critiques", "status": "à faire"},
            {"étape": "Prototyper chaque module", "status": "à faire"},
            {"étape": "Intégrer les modules dans une boucle logique", "status": "à faire"},
            {"étape": "Tester et corriger", "status": "à faire"},
            {"étape": "Réviser et améliorer", "status": "à faire"}
        ]

    def _ajuster_plan(self, plan: list) -> list:
        étapes = [étape["étape"].lower() for étape in plan]

        if not any("tester" in e for e in étapes):
            plan.append({"étape": "Tester et valider", "status": "à faire"})
        if not any("améliorer" in e for e in étapes):
            plan.append({"étape": "Améliorer l’approche", "status": "à faire"})

        return plan
