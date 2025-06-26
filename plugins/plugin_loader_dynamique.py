# plugins/plugin_loader_dynamique.py

from noyau_core import BasePlugin, Context, Meta

class PluginLoaderDynamique(BasePlugin):
    meta = Meta(
        name="plugin_loader_dynamique",
        version="1.0",
        priority=2.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        strategie = ctx.get("strategie_adaptive", {})
        a_prioriser = strategie.get("priorite", [])
        a_eviter = strategie.get("eviter", [])

        plugins_disponibles = ctx.get("plugins_disponibles", [])

        plugins_choisis = [
            nom for nom in plugins_disponibles
            if (not a_eviter or nom not in a_eviter) and
               (not a_prioriser or nom in a_prioriser)
        ]

        if not plugins_choisis:
            ctx["plugins_log"].append("PluginLoaderDynamique : aucun plugin actif sélectionné.")
        else:
            ctx["plugins_a_utiliser"] = plugins_choisis
            ctx["plugins_log"].append(f"PluginLoaderDynamique : plugins activés = {plugins_choisis}")

        return ctx
