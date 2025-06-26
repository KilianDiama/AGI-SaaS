from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.meta_pattern")

class PluginMetaPatternDetector(BasePlugin):
    meta = Meta(
        name="plugin_meta_pattern_detector",
        version="1.0",
        priority=2.7,  # Juste après la mémoire active et le raisonnement
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        messages = [item.get("message", "") for item in historique if item.get("from") == "user" or item.get("from") == "ai"]
        corpus = "\n".join(messages)

        alertes = self.detecter_patterns(corpus)

        ctx["meta_patterns"] = alertes
        ctx.setdefault("plugins_log", []).append("plugin_meta_pattern_detector : patterns analysés")
        logger.info(f"[meta_pattern] Alertes détectées : {alertes}")

        return ctx

    def detecter_patterns(self, texte: str) -> str:
        alertes = []

        if texte.count("je vais faire de mon mieux") >= 3:
            alertes.append("🔁 Répétition fréquente de formules génériques — signe de stagnation cognitive.")

        if re.search(r"\b(?:toujours|jamais)\b", texte, flags=re.IGNORECASE):
            alertes.append("🧠 Absolutisme détecté — possible simplification excessive du raisonnement.")

        if texte.lower().count("je ne suis qu'une ia") > 1:
            alertes.append("🤖 Répétition de l'humilité artificielle — à remplacer par des réponses assertives.")

        if not alertes:
            alertes.append("✅ Aucun pattern problématique détecté.")

        return "\n".join(alertes)
