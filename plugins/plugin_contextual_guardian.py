import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.contextual_guardian")

class PluginContextualGuardian(BasePlugin):
    meta = Meta(
        name="plugin_contextual_guardian",
        version="1.0",
        priority=4.6,  # Juste avant envoi final
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "").lower()
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        message = ctx.get("message", "").lower()
        response = ctx.get("response", "")
        plugins_log = ctx.setdefault("plugins_log", [])

        blocked = False
        alertes = []

        # Contradiction intention vs objectif
        if "jouer" in message and "répondre à une question sérieuse" in objectif:
            alertes.append("🎭 Conflit détecté entre intention ludique et objectif sérieux.")
            blocked = True

        # Contexte sensible mais réponse trop vague
        if "santé" in message or "malade" in message:
            if "je ne suis pas médecin" in response.lower() or "je ne peux pas aider" in response.lower():
                alertes.append("⚠️ Réponse d'évitement dans un contexte médical")
                blocked = True

        # Intention vide ou mauvaise détection
        if not intention or intention == "vide":
            alertes.append("❓ Intention non détectée ou absente")
            blocked = True

        # Historique contradictoire (futur : vérifier mémoire long terme)

        # Action selon gravité
        if blocked:
            ctx["response"] = "[🔐 Réponse bloquée : incohérence contextuelle détectée]"
            ctx["context_guardian_flags"] = alertes
            plugins_log.append("plugin_contextual_guardian : réponse bloquée pour incohérence")
            logger.warning(f"[contextual_guardian] Blocage forcé : {alertes}")
        else:
            plugins_log.append("plugin_contextual_guardian : OK")

        return ctx
