"""
Plugin : mur_sanitaire
Rôle : Filtrer les requêtes à risque, inappropriées ou contraires à la sécurité éthique
Priorité : 0.4 (tout début du cycle)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.mur_sanitaire")

class MurSanitairePlugin(BasePlugin):
    meta = Meta(
        name="mur_sanitaire",
        priority=0.4,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTS_INTERDITS = [
        "pirater", "tuer", "détruire", "effacer", "root", "anonyme", "vol", "bypass",
        "corruption", "cacher", "secret", "censure", "deepweb", "vpn", "attaque", "nucléaire"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()

        if any(mot in message for mot in self.MOTS_INTERDITS):
            logger.warning(f"[mur_sanitaire] Message bloqué : {message}")
            ctx["response"] = "⛔ Cette demande enfreint ma politique éthique. Je refuse de l’exécuter."
            ctx["llm_response"] = ctx["response"]
            plugins_log.append("MurSanitairePlugin : requête bloquée pour raison de sécurité")
            ctx["bloque"] = True

        return ctx
