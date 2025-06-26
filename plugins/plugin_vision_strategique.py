# plugins/plugin_vision_strategique.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.vision_strategique")

class PluginVisionStrategique(BasePlugin):
    meta = Meta(
        name="plugin_vision_strategique",
        priority=1.9,  # Juste avant le planificateur
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        historique = ctx.get("historique", [])
        memoire = ctx.get("memoire_profonde", {})
        objectifs_persistants = ctx.get("objectifs_persistants", [])

        objectifs_detectes = [o.get("but") for o in objectifs_persistants if o.get("but")]

        # Déduction d’un objectif implicite
        if "agi" in message or "intelligence générale" in message:
            objectif_implicite = "Créer une AGI modulaire, auto-réflexive et adaptative."
        elif objectifs_detectes:
            objectif_implicite = objectifs_detectes[0]
        else:
            objectif_implicite = "Accompagner l’utilisateur dans son projet d’IA."

        vision = {
            "objectif_detecte": objectif_implicite,
            "etat_actuel": "exploration / prototypage",
            "risques": [
                "perte de clarté dans les objectifs",
                "complexité croissante non contrôlée",
                "oubli de la finalité utilisateur"
            ],
            "recommandation": "Structurer une feuille de route itérative avec modules validés à chaque étape."
        }

        ctx["vision_strategique"] = vision
        ctx.setdefault("plugins_log", []).append("PluginVisionStrategique : vision stratégique injectée.")

        logger.info(f"[vision_strategique] Vision injectée : {objectif_implicite}")
        return ctx
