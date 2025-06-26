import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.anticipateur")

class PluginAnticipateur(BasePlugin):
    meta = Meta(
        name="plugin_anticipateur",
        version="1.0",
        priority=8.9,  # Juste avant la supervision finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.setdefault("plugins_log", [])
        anticipations = []

        plan = ctx.get("plan", [])
        tache = ctx.get("tache_courante", "")
        intention = ctx.get("intention", "")
        reflexion = ctx.get("reflexion_interne", "")
        erreurs = ctx.get("errors", [])
        historique = ctx.get("history", [])
        now = datetime.now()

        # Anticipation : boucle ou stagnation
        if plan and all(e["status"] == "fait" for e in plan):
            anticipations.append("🌀 Risque de boucle : toutes les étapes sont terminées.")
        elif not plan:
            anticipations.append("⚠️ Aucune stratégie active, risque de stagnation.")
        elif tache and tache.lower().startswith("collecter") and len(historique) > 3:
            anticipations.append("📎 Collecte prolongée : envisager une synthèse ou reformulation.")

        # Anticipation : sur-répétition ou confusion
        if reflexion and "objectif vague" in reflexion.lower():
            anticipations.append("❓ Objectif flou répété : proposer clarification à l’utilisateur.")
        if erreurs and len(erreurs) >= 3:
            anticipations.append("🚨 Erreurs récurrentes : suggérer redémarrage du cycle ou fallback.")

        # Injection d’un champ prédictif
        prediction = "\n".join(anticipations) or "✅ Aucun risque immédiat détecté."
        ctx["prediction_interne"] = prediction
        logs.append("plugin_anticipateur : prédiction comportementale injectée.")
        logger.info(f"[anticipateur] Prévision :\n{prediction}")

        return ctx
