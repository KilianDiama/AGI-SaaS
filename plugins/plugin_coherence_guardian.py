from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.coherence_guardian")

class PluginCoherenceGuardian(BasePlugin):
    meta = Meta(
        name="plugin_coherence_guardian",
        version="1.0",
        priority=3.9,  # Juste avant la fusion et après les réponses LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse = ctx.get("llm_response", "")
        contexte = ctx.get("context_injection", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        intention = ctx.get("intention", "")

        alertes = []

        if not reponse.strip():
            alertes.append("❌ Aucune réponse générée.")

        if objectif and objectif.lower() not in reponse.lower():
            alertes.append("⚠️ Réponse peut-être non alignée avec l’objectif.")

        if intention and intention.lower() not in reponse.lower():
            alertes.append("⚠️ L’intention de l’utilisateur ne semble pas prise en compte.")

        if contexte and any(
            mot.lower() not in reponse.lower() for mot in contexte.split()[:5]
        ):
            alertes.append("🔄 La réponse semble ignorer le contexte injecté.")

        if alertes:
            ctx["coherence_alertes"] = "\n".join(alertes)
            ctx.setdefault("plugins_log", []).append("PluginCoherenceGuardian : incohérences détectées.")
            logger.warning("[CoherenceGuardian] Problèmes détectés :\n" + "\n".join(alertes))
        else:
            ctx.setdefault("plugins_log", []).append("PluginCoherenceGuardian : réponse validée.")
            logger.info("[CoherenceGuardian] Réponse logique et cohérente.")

        return ctx
