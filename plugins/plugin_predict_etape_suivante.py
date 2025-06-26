import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.predict_etape_suivante")

class PluginPredictEtapeSuivante(BasePlugin):
    meta = Meta(
        name="plugin_predict_etape_suivante",
        version="1.0",
        priority=1.35,  # Juste après planificateur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        logs = ctx.setdefault("plugins_log", [])

        if not plan:
            logs.append("PluginPredictEtapeSuivante : aucun plan trouvé.")
            return ctx

        for step in plan:
            if step["status"] == "à faire":
                ctx["tache_courante"] = step["étape"]
                logs.append(f"PluginPredictEtapeSuivante : prochaine étape = {step['étape']}")
                logger.info(f"[predict_etape] Étape suivante prédite : {step['étape']}")
                return ctx

        ctx["tache_courante"] = None
        logs.append("PluginPredictEtapeSuivante : toutes les étapes sont déjà faites.")
        return ctx
