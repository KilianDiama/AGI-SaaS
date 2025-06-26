# plugins/plugin_predict_pipeline.py

from noyau_core import BasePlugin, Context, Meta

class PluginPredictPipeline(BasePlugin):
    meta = Meta(
        name="plugin_predict_pipeline",
        version="1.0",
        priority=10.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        intention = ctx.get("intention", "").lower()
        plugins_log = ctx.setdefault("plugins_log", [])

        prediction = []

        if "résumer" in objectif or "synthèse" in intention:
            prediction = ["plugin_summary_fusion", "plugin_memoire_synthetique"]
        elif "répondre" in intention:
            prediction = ["plugin_raisonneur", "plugin_verificateur_reponse"]
        elif "plan" in objectif:
            prediction = ["plugin_planificateur_dynamique", "plugin_suivi_progression_plan"]
        elif "analyse" in intention:
            prediction = ["plugin_analyse_semantique", "plugin_contextual_guardian"]
        else:
            prediction = ["plugin_raisonneur", "plugin_eval_qualite_reponse"]

        ctx["pipeline_prediction"] = prediction
        plugins_log.append(f"{self.meta.name} : plugins prédits = {prediction}")
        return ctx
