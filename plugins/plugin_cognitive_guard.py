import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cognitive_guard")

class PluginCognitiveGuard(BasePlugin):
    meta = Meta(
        name="plugin_cognitive_guard",
        version="1.0",
        priority=4.7,  # Juste avant le fusionneur et l'optimizer
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response") or ctx.get("llm_response_votée") or ""
        logs = ctx.setdefault("plugins_log", [])

        # Simulations simples de détection logique
        alerts = []

        if "je ne sais pas" in response.lower() and "voici la réponse" in response.lower():
            alerts.append("🔄 Contradiction : incertitude exprimée suivie d'une affirmation.")

        if any(p in response.lower() for p in ["certain", "toujours", "jamais"]) and "peut-être" in response.lower():
            alerts.append("🌀 Possible biais d’overconfiance mêlé à de l’incertitude.")

        if response.count("donc") >= 3 and response.count("car") == 0:
            alerts.append("🔁 Raisonnement circulaire possible (beaucoup de 'donc' sans justification).")

        if "erreur" in response.lower() and "corrigé" not in response.lower():
            alerts.append("⚠️ Mention d'erreur sans correction proposée.")

        # Résultat final
        if alerts:
            ctx["cognitive_warnings"] = alerts
            logs.append(f"PluginCognitiveGuard : {len(alerts)} incohérences détectées.")
            logger.warning("[cognitive_guard] Incohérences détectées :\n" + "\n".join(alerts))
        else:
            ctx["cognitive_warnings"] = []
            logs.append("PluginCognitiveGuard : aucune incohérence détectée.")
            logger.info("[cognitive_guard] Pas d’anomalies détectées.")

        return ctx
