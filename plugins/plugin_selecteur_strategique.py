# plugins/plugin_selecteur_strategique.py

from noyau_core import BasePlugin, Context, Meta

class PluginSelecteurStrategique(BasePlugin):
    meta = Meta(
        name="plugin_selecteur_strategique",
        version="1.0",
        priority=2.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        stats = ctx.get("meta_apprentissage_stats", {})

        meilleures = stats.get("meilleures_actions", [])
        pires = stats.get("pires_actions", [])

        if not meilleures:
            ctx["plugins_log"].append("PluginSelecteurStrategique : aucune stratégie fiable trouvée.")
            return ctx

        # Extraire les meilleures stratégies à prioriser
        top_actions = [action for action, note in meilleures if note >= 3.0]

        # Mettre à jour le contexte avec les stratégies recommandées
        ctx["strategie_adaptive"] = {
            "priorite": top_actions,
            "eviter": [a for a, _ in pires],
            "origine": "meta_apprentissage_stats"
        }

        ctx["plugins_log"].append(f"PluginSelecteurStrategique : stratégies recommandées = {top_actions}")
        return ctx
