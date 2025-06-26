import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conseiller_strategique")

class PluginConseillerStrategique(BasePlugin):
    meta = Meta(
        name="plugin_conseiller_strategique",
        version="1.0",
        priority=2.0,  # Avant style, raisonneur et fusion
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "")
        tonalite = ctx.get("tonalite_utilisateur", "neutre")
        reflexion = ctx.get("reflexion_interne", "")
        plugins = []

        # 🔍 Analyse stratégique selon intention
        if "explication" in intention or "apprendre" in intention:
            plugins.append("plugin_explainer_llm")
        if "résumé" in intention or "synthèse" in reflexion:
            plugins.append("plugin_summarizer_pro")
        if tonalite == "négative":
            plugins.append("plugin_empatie_response")

        # 🎯 Recommandation mémoire contextuelle
        if "ancien message" in reflexion or "mémoire absente" in reflexion:
            plugins.append("plugin_memory_importer")

        if plugins:
            ctx.setdefault("strategic_recommendations", []).extend(plugins)
            ctx.setdefault("plugins_log", []).append(
                f"PluginConseillerStrategique : recommandations = {plugins}"
            )
            logger.info(f"[conseiller] Recommandations stratégiques : {plugins}")
        else:
            logger.info("[conseiller] Aucune recommandation nécessaire.")

        return ctx
