# plugins/plugin_adaptateur_pipeline_dynamique.py

from noyau_core import BasePlugin, Context, Meta

class PluginAdaptateurPipelineDynamique(BasePlugin):
    meta = Meta(
        name="plugin_adaptateur_pipeline_dynamique",
        version="1.0",
        priority=10.1,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prediction = ctx.get("pipeline_prediction", [])
        pipeline_actif = ctx.setdefault("pipeline_actif", [])
        plugins_log = ctx.setdefault("plugins_log", [])

        if not prediction:
            plugins_log.append(f"{self.meta.name} : aucune prédiction à appliquer.")
            return ctx

        # Suppression des plugins non pertinents
        nouveaux_plugins = list(set(pipeline_actif + prediction))
        ctx["pipeline_actif"] = prediction  # On remplace pour forcer la cohérence
        plugins_log.append(f"{self.meta.name} : pipeline ajusté dynamiquement → {prediction}")
        return ctx
