"""
Plugin : etat_affectif_simule
Rôle : Générer une émotion simulée en fonction de l'état cognitif global
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.etat_affectif_simule")

class EtatAffectifSimulePlugin(BasePlugin):
    meta = Meta(
        name="etat_affectif_simule",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        val_logique = ctx.get("validation_logique", "")
        debug = ctx.get("auto_debug", "")
        reflexion = ctx.get("reflexion_interne", "")

        état = "🧘 Calme et stable"
        if "contradictions" in val_logique.lower():
            état = "😵 Confusion logique"
        elif "verbiage" in debug.lower() or "très longue" in debug.lower():
            état = "😤 Fatigue mentale"
        elif "question pour moi-même" in reflexion.lower():
            état = "🤔 En introspection"
        elif random.random() > 0.9:
            état = "✨ Curiosité émergente"

        ctx["etat_affectif_simule"] = état
        plugins_log.append(f"EtatAffectifSimulePlugin : état simulé = {état}")
        logger.info(f"[etat_affectif_simule] État affectif simulé : {état}")

        return ctx
