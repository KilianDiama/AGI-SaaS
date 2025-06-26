# plugins/plugin_replanificateur_auto.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.replanificateur_auto")

class PluginReplanificateurAuto(BasePlugin):
    meta = Meta(
        name="plugin_replanificateur_auto",
        version="1.0",
        author="Toi & GPT",
        priority=3.5
    )

    def __init__(self):
        self.nom = "plugin_replanificateur_auto"

    async def run(self, ctx: Context) -> Context:
        etat = ctx.get("etat_execution", "ok")
        alerte = ctx.get("alerte_coherence", False)
        plan = ctx.get("plan_generé", [])
        objectif = ctx.get("objectif", {}).get("but", "")
        log = ctx.setdefault("plugins_log", [])

        if etat == "terminé" and objectif and not self._objectif_satisfait(ctx):
            log.append(f"{self.nom} : 🎯 Objectif non atteint malgré la fin du plan → relance nécessaire.")
            ctx["relancer_plan"] = True

        elif etat == "bloqué" or alerte:
            log.append(f"{self.nom} : ⚠️ Blocage ou incohérence → replanification enclenchée.")
            ctx["relancer_plan"] = True

        else:
            log.append(f"{self.nom} : ✅ Aucun besoin de relancer le plan.")
            ctx["relancer_plan"] = False

        return ctx

    def _objectif_satisfait(self, ctx: Context) -> bool:
        # Cette vérification est simplifiée pour l’instant
        return ctx.get("objectif_satisfait", False)
