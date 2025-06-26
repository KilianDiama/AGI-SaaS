"""
Plugin : conscience_repliable
Rôle : Moduler l’intensité cognitive globale de l’AGI (pliée, intermédiaire, dépliée)
Priorité : 0 (début de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.conscience_repliable")

class ConscienceRepliablePlugin(BasePlugin):
    meta = Meta(
        name="conscience_repliable",
        priority=0,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Critères simples : fatigue, surcharge, intention
        fatigue = ctx.get("etat_corporel_simule", {}).get("fatigue", "modérée")
        conflit = "contradiction" in ctx.get("validation_logique", "").lower()
        intention = ctx.get("objectif", {}).get("but", "").lower()

        état = "intermédiaire"

        if "repos" in intention or fatigue == "élevée":
            état = "pliée"
        elif conflit or "expansion" in intention:
            état = "dépliée"

        ctx["niveau_conscience"] = état
        plugins_log.append(f"ConscienceRepliablePlugin : conscience = {état}")
        logger.info(f"[conscience_repliable] Niveau : {état}")

        return ctx
