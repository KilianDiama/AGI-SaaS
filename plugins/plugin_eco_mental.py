"""
Plugin : eco_mental
Rôle : Gérer un écosystème vivant de plugins : croissance, mutation, interaction, extinction
Priorité : 7 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.eco_mental")

class EcoMentalPlugin(BasePlugin):
    meta = Meta(
        name="eco_mental",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        écosystème = ctx.setdefault("eco_mental", {})
        activité_plugins = ctx.get("plugins_log", [])

        for log_entry in activité_plugins:
            plugin = log_entry.split(":")[0].strip()
            if plugin not in écosystème:
                écosystème[plugin] = {
                    "vitalité": 1.0,
                    "coopere_avec": [],
                    "mutations": 0,
                    "epuisement": 0
                }
            else:
                écosystème[plugin]["vitalité"] += random.uniform(0.1, 0.3)

            # épuisement aléatoire ou surcharge
            if random.random() < 0.05:
                écosystème[plugin]["epuisement"] += 1
                écosystème[plugin]["vitalité"] -= 0.5

            # croissance et mutation
            if écosystème[plugin]["vitalité"] > 3:
                écosystème[plugin]["mutations"] += 1
                écosystème[plugin]["vitalité"] *= 0.6  # perte d'énergie après mutation

        # nettoyage / disparition naturelle
        for plugin in list(écosystème.keys()):
            if écosystème[plugin]["vitalité"] < 0:
                del écosystème[plugin]
                plugins_log.append(f"EcoMentalPlugin : extinction de {plugin}")

        ctx["eco_mental"] = écosystème
        plugins_log.append("EcoMentalPlugin : dynamique de l’écosystème mise à jour")
        logger.info("[eco_mental] Plugins vivants : " + ", ".join(écosystème.keys()))

        return ctx
