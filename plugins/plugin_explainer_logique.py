import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.explainer_logique")

class PluginExplainerLogique(BasePlugin):
    meta = Meta(
        name="plugin_explainer_logique",
        version="1.0",
        priority=4.1,  # Juste après vote_confiance et guardrails
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response", "")
        intention = ctx.get("intention", "générale")
        objectif = ctx.get("objectif", {}).get("but", "")
        reflexion = ctx.get("reflexion_interne", "")
        score = ctx.get("evaluation_reponse", {}).get("note", "inconnu")

        if not response.strip():
            logger.warning("[plugin_explainer_logique] Aucune réponse détectée pour explication.")
            ctx.setdefault("plugins_log", []).append("PluginExplainerLogique : rien à expliquer")
            return ctx

        explanation = (
            "🔍 **Explication du raisonnement :**\n\n"
            f"- 🎯 **Intention détectée** : {intention or 'non précisée'}\n"
            f"- 📌 **Objectif assigné** : {objectif or 'non défini'}\n"
            f"- 🤔 **Réflexion interne** : {reflexion or 'pas de réflexion'}\n"
            f"- ✅ **Qualité estimée de la réponse** : {score}/5\n"
            f"- 🧾 **Résumé de la sortie** :\n> {response[:180]}{'...' if len(response) > 180 else ''}\n"
        )

        ctx["explication_logique"] = explanation
        ctx.setdefault("plugins_log", []).append("PluginExplainerLogique : explication générée")
        logger.info("[explainer_logique] Explication logique générée.")

        return ctx
