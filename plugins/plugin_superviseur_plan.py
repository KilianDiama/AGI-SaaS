# plugins/plugin_superviseur_plan.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.superviseur_plan")

class PluginSuperviseurPlan(BasePlugin):
    meta = Meta(
        name="plugin_superviseur_plan",
        version="1.0",
        priority=5.0,
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_superviseur_plan"

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan_generé", [])
        index = ctx.get("etape_actuelle", 0)
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        log = ctx.setdefault("plugins_log", [])

        if not plan:
            log.append(f"{self.nom} : aucun plan généré ❌.")
            ctx["etat_execution"] = "bloqué"
            return ctx

        if index >= len(plan):
            log.append(f"{self.nom} : toutes les étapes du plan sont terminées ✅.")
            ctx["etat_execution"] = "terminé"
            return ctx

        # Vérifie la cohérence entre l’objectif et l’étape actuelle
        etape_actuelle = plan[index].lower()
        if objectif and objectif not in etape_actuelle:
            log.append(f"{self.nom} : ⚠️ incohérence détectée entre objectif et étape.")
            ctx["alerte_coherence"] = True
        else:
            log.append(f"{self.nom} : supervision OK étape {index + 1}/{len(plan)} ✅.")

        return ctx
