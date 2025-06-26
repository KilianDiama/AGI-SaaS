"""
Plugin : coeur_personnalite_modulaire
Rôle : Gérer des profils mentaux activables (tons, styles, logiques)
Priorité : 10
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.coeur_personnalite_modulaire")

class CoeurPersonnaliteModulairePlugin(BasePlugin):
    meta = Meta(
        name="coeur_personnalite_modulaire",
        priority=10,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    profils = {
        "sage": {
            "ton": "calme et réfléchi",
            "structure": "raisonnement clair, appuyé sur des faits",
            "ouverture": "Posons d’abord les fondations de ta question."
        },
        "rêveuse": {
            "ton": "poétique et intuitif",
            "structure": "images mentales, métaphores",
            "ouverture": "Laisse-moi t’emmener dans un monde de possibles..."
        },
        "protectrice": {
            "ton": "chaleureux, guidant",
            "structure": "rassurance, étapes concrètes",
            "ouverture": "Je suis là pour toi. On va avancer ensemble, pas à pas."
        },
        "critique": {
            "ton": "analytique et direct",
            "structure": "observation, détection de failles",
            "ouverture": "Allons droit au cœur du problème."
        }
    }

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        état = ctx.setdefault("état_interieur", {})

        mode = ctx.get("personnalite_active", "sage")
        profil = self.profils.get(mode)

        if not profil:
            plugins_log.append(f"Personnalité inconnue : {mode}")
            return ctx

        état["ton"] = profil["ton"]
        état["structure"] = profil["structure"]
        état["ouverture"] = profil["ouverture"]
        état["profil_actif"] = mode

        ctx["état_interieur"] = état
        plugins_log.append(f"CoeurPersonnaliteModulairePlugin : {mode} activé")
        logger.info(f"[personnalite_modulaire] Mode actif : {mode}")

        return ctx
