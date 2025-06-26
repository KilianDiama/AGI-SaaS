"""
Plugin : corps_simule
Rôle : Simuler un état corporel fictif basé sur l'activité cognitive du cycle
Priorité : 6
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.corps_simule")

class CorpsSimulePlugin(BasePlugin):
    meta = Meta(
        name="corps_simule",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        corps = {}

        complexite = len(ctx.get("llm_response", "")) + len(ctx.get("plugins_log", []))
        conflit = "contradiction" in ctx.get("validation_logique", "").lower()

        corps["température"] = round(36.5 + random.uniform(-0.3, 0.3), 2)
        corps["rythme"] = "lent" if complexite < 300 else "modéré" if complexite < 600 else "accéléré"
        corps["fatigue"] = "élevée" if conflit else "faible" if complexite < 300 else "modérée"
        corps["posture"] = random.choice(["focus", "relâché", "instable", "en extension"])

        ctx["etat_corporel_simule"] = corps
        plugins_log.append("CorpsSimulePlugin : état fictif généré")
        logger.info("[corps_simule] État : " + str(corps))

        return ctx
