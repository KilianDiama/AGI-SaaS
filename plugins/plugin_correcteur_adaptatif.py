import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.correcteur_adaptatif")

class PluginCorrecteurAdaptatif(BasePlugin):
    meta = Meta(
        name="plugin_correcteur_adaptatif",
        version="1.0",
        priority=9.0,  # Juste après l'anticipateur, avant la clôture du cycle
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prediction = ctx.get("prediction_interne", "")
        plan = ctx.get("plan", [])
        reflexion = ctx.get("reflexion_interne", "")
        plugins_log = ctx.setdefault("plugins_log", [])

        corrections = []

        if "boucle" in prediction.lower():
            corrections.append("🔁 Redémarrage du plan.")
            for step in plan:
                step["status"] = "à faire"
            ctx["plan"] = plan

        if "objectif flou" in prediction.lower() or "objectif vague" in reflexion.lower():
            corrections.append("🧭 Suggestion : demander à l’utilisateur de préciser l’objectif.")
            ctx["message_suggestion"] = "Ton objectif semble flou, veux-tu le reformuler ?"

        if "aucune stratégie" in prediction.lower():
            corrections.append("📋 Création d’un mini-plan de secours.")
            ctx["plan"] = [
                {"étape": "clarifier l’intention", "status": "à faire"},
                {"étape": "réévaluer le contexte", "status": "à faire"},
                {"étape": "relancer l’analyse", "status": "à faire"},
            ]

        ctx["corrections_appliquées"] = corrections or ["✅ Aucune correction nécessaire."]
        plugins_log.append("plugin_correcteur_adaptatif : corrections adaptatives appliquées.")
        logger.info(f"[correcteur] Actions : {ctx['corrections_appliquées']}")

        return ctx
