"""
Plugin : optimisation_energie
Rôle : Réduire les calculs inutiles si une réponse claire et rapide est possible
Priorité : 1.3 (très tôt dans le cycle cognitif)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.optimisation_energie")

class OptimisationEnergiePlugin(BasePlugin):
    meta = Meta(
        name="optimisation_energie",
        priority=1.3,
        version="1.0",
        author="AGI & Matthieu"
    )

    PHRASES_DIRECTES = [
        "quel est ton nom", "qui t’a créé", "donne la date", "quel est ton rôle",
        "définis", "définition de", "qui suis-je", "combien font", "quelle heure"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").strip().lower()

        if any(phrase in message for phrase in self.PHRASES_DIRECTES):
            ctx["reponse_directe"] = True
            plugins_log.append("OptimisationEnergiePlugin : réponse directe possible → raccourci activé")
            logger.info("[optimisation_energie] Raccourci cognitif activé")
        else:
            ctx["reponse_directe"] = False
            plugins_log.append("OptimisationEnergiePlugin : aucun raccourci applicable.")

        return ctx
