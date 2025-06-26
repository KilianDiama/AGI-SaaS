""" 
Plugin : exploration_externe  
Rôle : Suggérer une action ou recherche vers l’extérieur si besoin d’info détecté  
Priorité : 5.5 (après raisonnement, avant création)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.exploration_externe")

class ExplorationExternePlugin(BasePlugin):
    meta = Meta(
        name="exploration_externe",
        priority=5.5,
        version="1.1",  # ← mise à jour de version
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif", "")
        reponse = ctx.get("response", "")

        # Sécurité : vérifier que ce sont bien des chaînes avant .lower()
        if not isinstance(objectif, str):
            objectif = str(objectif)
        if not isinstance(reponse, str):
            reponse = str(reponse)

        objectif = objectif.lower()
        reponse = reponse.lower()

        mots_clés = ["inconnu", "non défini", "à chercher", "besoin", "?"]
        manque_detecte = any(mot in objectif for mot in mots_clés) or any(mot in reponse for mot in mots_clés)

        if not manque_detecte:
            plugins_log.append("ExplorationExternePlugin : pas de besoin d’exploration détecté.")
            return ctx

        suggestion = (
            "🔍 Suggestion d'exploration :\n"
            "→ Interroger une source externe (API, site, documentation) pour compléter l'information.\n"
            f"Objectif : « {objectif[:60]}... »"
        )

        ctx["exploration_suggeree"] = suggestion
        if not ctx.get("response"):
            ctx["response"] = suggestion

        plugins_log.append("ExplorationExternePlugin : exploration externe suggérée.")
        logger.info("[exploration_externe] Suggestion injectée.")

        return ctx
