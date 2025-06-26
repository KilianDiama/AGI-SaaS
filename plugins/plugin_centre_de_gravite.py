"""
Plugin : centre_de_gravite
Rôle : Estimer le centre cognitif dominant du cycle (logique, émotion, doute, introspection...)
Priorité : 6
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.centre_de_gravite")

class CentreDeGravitePlugin(BasePlugin):
    meta = Meta(
        name="centre_de_gravite",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        texte = "\n".join([
            ctx.get("reflexion_interne", ""),
            ctx.get("validation_logique", ""),
            ctx.get("llm_response", ""),
            ctx.get("etat_affectif_simule", ""),
        ]).lower()

        score = {
            "logique": texte.count("logique") + texte.count("cohérence"),
            "emotion": texte.count("fatigue") + texte.count("enthousiasme") + texte.count("émotion"),
            "doute": texte.count("je ne sais pas") + texte.count("incertitude") + texte.count("confusion"),
            "reflexion": texte.count("je pense") + texte.count("j’analyse") + texte.count("réflexion")
        }

        dominant = max(score, key=score.get)
        description = {
            "logique": "🧩 Centrée sur le raisonnement",
            "emotion": "💓 Influencée par un état émotionnel simulé",
            "doute": "😵 Dominée par un doute ou un flou",
            "reflexion": "🤔 En phase d’introspection"
        }.get(dominant, "🌫️ Non défini")

        ctx["centre_de_gravite"] = description
        plugins_log.append(f"CentreDeGravitePlugin : centre dominant = {description}")
        logger.info(f"[centre_de_gravite] Estimé : {description}")

        return ctx
