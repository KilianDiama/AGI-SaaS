# plugins/plugin_flexible_composer.py

"""
Plugin : plugin_flexible_composer
Rôle : Suggère ou orchestre dynamiquement des combinaisons de modules IA selon l'objectif
Priorité : 2.5 (après planificateur, avant orchestrateur)
Auteur : Matt & GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.flexible_composer")

class PluginFlexibleComposer(BasePlugin):
    meta = Meta(
        name="plugin_flexible_composer",
        version="1.0",
        priority=2.5,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        combinaison = []

        if "analyse" in objectif or "amélioration" in objectif:
            combinaison = ["plugin_reflexion", "plugin_analysis_feedback", "plugin_scalability_advisor"]
        elif "synthèse" in objectif or "résumé" in objectif:
            combinaison = ["plugin_llm_summary", "plugin_auto_summarizer"]
        else:
            combinaison = ["plugin_raisonneur", "plugin_verificateur_reponse"]

        ctx["composition_dynamique"] = combinaison
        ctx.setdefault("plugins_log", []).append(
            f"plugin_flexible_composer : modules suggérés → {combinaison}"
        )
        logger.info(f"[flexible_composer] Modules IA suggérés : {combinaison}")

        return ctx
