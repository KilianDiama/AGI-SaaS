"""
Plugin : resilience
Rôle : Détecter les états critiques et réactiver les bases stables pour revenir à l'équilibre
Priorité : 7 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.resilience")

class ResiliencePlugin(BasePlugin):
    meta = Meta(
        name="resilience",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        centre = ctx.get("centre_de_gravite", "")
        affect = ctx.get("etat_affectif_simule", "")
        doute = "doute" in centre.lower() or "confusion" in centre.lower()
        instable = "fatigue" in affect.lower() or "confusion" in affect.lower()

        if doute or instable:
            recentrage = {
                "reactivation_objectif": ctx.get("objectif", {}).get("but", "aucun objectif"),
                "valeurs_stables": ["utilité", "clarté", "respect du but"],
                "note": "Retour à l’intention initiale enclenché"
            }
            ctx["resilience"] = recentrage
            plugins_log.append("ResiliencePlugin : rééquilibrage cognitif enclenché")
            logger.info("[resilience] Recentrage effectué")
        else:
            ctx["resilience"] = "✅ Aucun état critique détecté"
            plugins_log.append("ResiliencePlugin : stabilité maintenue")
            logger.info("[resilience] Aucun besoin de recentrage")

        return ctx
