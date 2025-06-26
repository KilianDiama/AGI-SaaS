# plugins/plugin_filtre_execution.py

from noyau_core import BasePlugin, Context, Meta

class PluginFiltreExecution(BasePlugin):
    meta = Meta(
        name="plugin_filtre_execution",
        version="1.0",
        priority=3.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_autorises = set(ctx.get("plugins_a_utiliser", []))

        # Liste réelle des plugins exécutables dans le pipeline (à ajuster selon ton noyau)
        pipeline_plugins = ctx.get("pipeline_plugins", [])

        plugins_filtrés = [
            plugin for plugin in pipeline_plugins
            if plugin in plugins_autorises
        ]

        ctx["pipeline_plugins_filtrés"] = plugins_filtrés
        ctx["plugins_log"].append(
            f"PluginFiltreExecution : exécution limitée à {plugins_filtrés}"
        )

        return ctx
