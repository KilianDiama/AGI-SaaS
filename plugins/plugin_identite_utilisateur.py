# plugins/plugin_identite_utilisateur.py

"""
Plugin : identite_utilisateur
Rôle   : Injecte et distingue l'identité de l'utilisateur dans le contexte
Priorité : -99 (très en amont)
Auteur  : Toi + GPT
"""

from noyau_core import BasePlugin, Context, Meta

class IdentiteUtilisateurPlugin(BasePlugin):
    meta = Meta(
        name="identite_utilisateur",
        priority=-99,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        user_id = ctx.get("user_id", "anonyme")
        session_id = ctx.get("session_id", "session-temp")

        ctx["identite_utilisateur"] = {
            "user_id": user_id,
            "session_id": session_id
        }

        return ctx
