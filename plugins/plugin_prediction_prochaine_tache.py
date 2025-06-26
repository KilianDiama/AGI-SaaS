from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.prediction_tache")

class PluginPredictionProchaineTache(BasePlugin):
    meta = Meta(
        name="plugin_prediction_prochaine_tache",
        version="1.0",
        priority=3.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        etape = ctx.get("tache_courante", "")
        prediction = ""

        if not plan or not etape:
            prediction = "formuler un plan"
        else:
            prochaines = [step["étape"] for step in plan if step["status"] == "à faire"]
            prediction = prochaines[0] if prochaines else "finaliser réponse"

        ctx["tache_suggeree"] = prediction
        ctx.setdefault("plugins_log", []).append(
            f"PluginPredictionProchaineTache : prochaine étape = {prediction}"
        )
        logger.info(f"[prediction_tache] Étape suivante suggérée : {prediction}")
        return ctx
