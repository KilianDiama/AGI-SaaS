import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.opportuniste")

class PluginOpportuniste(BasePlugin):
    meta = Meta(
        name="plugin_opportuniste",
        version="1.0",
        priority=8.9,  # Avant la synthèse finale mais après réflexion/logique
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        current_hour = datetime.now().hour
        intention = ctx.get("intention", "")
        last_eval = ctx.get("evaluation_reponse", {}).get("note", 0)

        opportunite = ""

        # Détection d’opportunité selon l'heure
        if 9 <= current_hour <= 11 or 14 <= current_hour <= 16:
            opportunite += "🕒 Moment optimal (haute attention humaine). "

        # Intention favorable à des suggestions ?
        if "proposer" in intention.lower() or "aider" in intention.lower():
            opportunite += "💡 L’intention invite à l’initiative. "

        # Score faible → possible relance ?
        if last_eval <= 2:
            opportunite += "⚠️ Dernière réponse peu utile, chance de mieux faire. "

        # Proposer ?
        if opportunite:
            ctx["opportunite_detectee"] = opportunite.strip()
            plugins_log.append(f"plugin_opportuniste : opportunité identifiée → {opportunite.strip()}")
            logger.info(f"[plugin_opportuniste] Opportunité détectée : {opportunite.strip()}")
        else:
            plugins_log.append("plugin_opportuniste : aucune fenêtre détectée")

        return ctx
