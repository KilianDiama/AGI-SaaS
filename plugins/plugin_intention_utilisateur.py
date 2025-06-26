"""
Plugin : intention_utilisateur
Rôle : Déduire l'intention sous-jacente du message utilisateur (ton, but, urgence)
Priorité : 1 (juste après réception du message)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.intention_utilisateur")

class IntentionUtilisateurPlugin(BasePlugin):
    meta = Meta(
        name="intention_utilisateur",
        priority=1,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("user_message", "").lower()

        if not message.strip():
            ctx["intention_utilisateur"] = "🔴 Aucun message à analyser."
            plugins_log.append("IntentionUtilisateurPlugin : aucun message fourni")
            return ctx

        # Analyse simple d’intentions implicites
        intention = []

        if "?" in message:
            intention.append("🔍 Question / recherche d'information")

        if "aide" in message or "besoin" in message:
            intention.append("🤝 Demande d'assistance")

        if "urgent" in message or "vite" in message:
            intention.append("⚠️ Sentiment d'urgence")

        if "je veux" in message or "j'aimerais" in message:
            intention.append("🎯 Expression de volonté")

        if not intention:
            intention.append("🧩 Intention implicite non identifiée — tonalité neutre ou complexe")

        ctx["intention_utilisateur"] = ", ".join(intention)
        plugins_log.append("IntentionUtilisateurPlugin : intention détectée")
        logger.info("[intention_utilisateur] Intention détectée : " + ctx["intention_utilisateur"])

        return ctx
