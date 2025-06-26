import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.guidance_user")

class PluginGuidanceUser(BasePlugin):
    meta = Meta(
        name="plugin_guidance_user",
        version="1.0",
        priority=9.3,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "")
        response = ctx.get("response", "")
        suggestions = []

        if not response:
            ctx["guidance"] = ["💡 Aucune réponse générée. Réessaie avec une formulation différente."]
            return ctx

        # Suggestions générales selon intention
        if intention == "générale":
            suggestions.append("🔁 Reformuler la question pour plus de précision.")
            suggestions.append("🔍 Voir les sources ou les modèles utilisés.")
            suggestions.append("📝 Demander un résumé ou une version simplifiée.")

        if "plugins_log" in ctx and any("erreur" in p.lower() for p in ctx["plugins_log"]):
            suggestions.append("🚧 Corriger les erreurs techniques détectées.")
        
        # Suggestions si longue réponse
        if len(response) > 500:
            suggestions.append("📄 Générer un résumé rapide.")
            suggestions.append("🧠 Sauvegarder cette réponse pour la suite.")

        # Historique
        if "history" in ctx and len(ctx["history"]) >= 3:
            suggestions.append("📂 Revenir à une question précédente.")
            suggestions.append("🔄 Comparer cette réponse avec une autre version.")

        ctx["guidance"] = suggestions or ["🤔 Aucun conseil disponible."]
        ctx.setdefault("plugins_log", []).append("PluginGuidanceUser : suggestions injectées")
        logger.info(f"[guidance_user] Suggestions : {suggestions}")

        return ctx
