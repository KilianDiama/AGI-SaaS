"""
Plugin : apprentissage_explicite
Rôle : Demander l'autorisation explicite d'apprendre une information nouvelle détectée
Priorité : 3.9 (après génération de réponse, avant enregistrement)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.apprentissage_explicite")

class ApprentissageExplicitePlugin(BasePlugin):
    meta = Meta(
        name="apprentissage_explicite",
        priority=3.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTS_CLES_APPRENTISSAGE = [
        "mon nom est", "je suis ton créateur", "je préfère", "je veux que tu te souviennes", "souviens-toi que"
    ]

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        plugins_log = ctx.setdefault("plugins_log", [])
        demandes = ctx.setdefault("requete_apprentissage", [])

        for phrase in self.MOTS_CLES_APPRENTISSAGE:
            if phrase in message:
                demandes.append(
                    f"Souhaites-tu que je retienne ceci pour plus tard ? ({phrase})"
                )
                plugins_log.append("ApprentissageExplicitePlugin : demande d'autorisation d'apprentissage générée.")
                logger.info(f"[apprentissage_explicite] Apprentissage potentiel détecté via '{phrase}'")
                break

        return ctx
