"""
Plugin : capacites_cartographie
Rôle : Dresser une carte interne des capacités connues, absentes ou inactives
Priorité : 0 (base du cycle)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.capacites_cartographie")

class CapacitesCartographiePlugin(BasePlugin):
    meta = Meta(
        name="capacites_cartographie",
        priority=0,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        loaded_plugins = ctx.get("plugins_loaded", [])
        known_modules = [
            "memoire", "objectifs", "reflexion", "simulation", "style", "evaluation",
            "planification", "perception", "feedback", "identite", "strategie"
        ]

        # Analyse des capacités perçues
        capacites = {
            "actives": [],
            "absentes": [],
            "inconnues": []
        }

        for module in known_modules:
            if any(module in p for p in loaded_plugins):
                capacites["actives"].append(module)
            else:
                capacites["absentes"].append(module)

        autres = [p for p in loaded_plugins if not any(k in p for k in known_modules)]
        if autres:
            capacites["inconnues"] = autres

        ctx["capacites_cartographie"] = capacites
        plugins_log.append("CapacitesCartographiePlugin : cartographie générée")
        logger.info("[capacites_cartographie] Capacités mappées")

        return ctx
