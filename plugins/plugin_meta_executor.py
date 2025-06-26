# plugins/plugin_meta_executor.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.meta_executor")

class PluginMetaExecutor(BasePlugin):
    meta = Meta(
        name="plugin_meta_executor",
        version="1.0",
        priority=101.5,  # Après PluginLoopManager
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        current_objectif = ctx.get("objectif_actuel")
        if not current_objectif:
            ctx.setdefault("plugins_log", []).append("PluginMetaExecutor : aucun objectif à exécuter.")
            return ctx

        # Exemple : Mapping des objectifs vers des plugins
        plan_plugins = {
            "analyser": ["plugin_analyse_semantique"],
            "résumer": ["plugin_memoire_synthetique"],
            "répondre": ["plugin_raisonneur", "plugin_verificateur_reponse"],
            "planifier": ["plugin_planificateur_contextuel"],
        }

        # Choix heuristique simple basé sur mots-clés
        triggered = []
        for mot_clé, plugins in plan_plugins.items():
            if mot_clé in current_objectif.lower():
                ctx.setdefault("plugins_forcés", []).extend(plugins)
                triggered = plugins
                break

        if triggered:
            ctx.setdefault("plugins_log", []).append(f"PluginMetaExecutor : plugins déclenchés → {triggered}")
        else:
            ctx.setdefault("plugins_log", []).append("PluginMetaExecutor : aucun plugin associé à cet objectif.")

        return ctx
