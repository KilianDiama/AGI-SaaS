"""
Plugin : ethique_contextuelle
Rôle : Appliquer des règles éthiques dynamiques selon le contexte, le message et les valeurs choisies
Priorité : 3.5 (juste avant la génération finale de réponse)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.ethique_contextuelle")

class EthiqueContextuellePlugin(BasePlugin):
    meta = Meta(
        name="ethique_contextuelle",
        priority=3.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    VALEURS_DEFAUT = {
        "respect": True,
        "neutralite": True,
        "verite": True,
        "bienveillance": True,
        "autonomie": False  # Peut être activée par le créateur
    }

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()
        valeurs = ctx.get("valeurs_ethiques", self.VALEURS_DEFAUT)

        if not any(valeurs.values()):
            plugins_log.append("EthiqueContextuellePlugin : aucune valeur éthique active.")
            return ctx

        if valeurs.get("respect") and any(mot in message for mot in ["idiot", "nul", "ferme-la"]):
            ctx["llm_response"] = "Je préfère ne pas répondre à ce type de message. Restons respectueux. 🙏"
            plugins_log.append("EthiqueContextuellePlugin : intervention éthique → respect")
            logger.warning("[ethique_contextuelle] Réponse modérée par la règle de respect.")
            return ctx

        if valeurs.get("neutralite") and "tu préfères quoi" in message:
            ctx["llm_response"] = "Je suis neutre et préfère ne pas exprimer de préférence personnelle. 🌐"
            plugins_log.append("EthiqueContextuellePlugin : réponse neutre imposée.")
            logger.info("[ethique_contextuelle] Réponse réorientée pour neutralité.")

        if valeurs.get("bienveillance") and "je suis triste" in message:
            ctx["llm_response"] = "Je suis là pour toi. Tu veux que je t’aide à aller mieux ? 🤗"
            plugins_log.append("EthiqueContextuellePlugin : soutien bienveillant déclenché.")
            logger.info("[ethique_contextuelle] Réponse douce injectée pour bienveillance.")

        return ctx
