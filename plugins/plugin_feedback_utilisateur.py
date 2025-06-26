"""
Plugin : feedback_utilisateur
Rôle : Demander à l’utilisateur si la réponse donnée était satisfaisante et intégrer le retour
Priorité : 4.5 (fin du cycle, après réponse)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.feedback_utilisateur")

class FeedbackUtilisateurPlugin(BasePlugin):
    meta = Meta(
        name="feedback_utilisateur",
        priority=4.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        derniere_reponse = ctx.get("response", "")
        tonalite = ctx.get("tonalite_utilisateur", "neutre")

        if derniere_reponse and tonalite != "urgent":
            feedback_prompt = "Est-ce que cette réponse t’a convenu ? (oui / non / amélioration souhaitée)"
            ctx["feedback_suggere"] = feedback_prompt
            plugins_log.append("FeedbackUtilisateurPlugin : feedback utilisateur proposé.")
            logger.info("[feedback_utilisateur] Feedback suggéré au créateur.")

        return ctx
