# plugins/plugin_simulateur_hypotheses.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.simulateur_hypotheses")

class PluginSimulateurHypotheses(BasePlugin):
    meta = Meta(
        name="plugin_simulateur_hypotheses",
        priority=2.4,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message_utilisateur = ctx.get("message", "")
        if not message_utilisateur:
            ctx.setdefault("plugins_log", []).append("PluginSimulateurHypotheses : message utilisateur manquant.")
            return ctx

        # Génération des hypothèses
        h1 = f"Réponse factuelle simple à : {message_utilisateur}"
        h2 = f"Réponse détaillée et contextuelle à : {message_utilisateur}"
        h3 = f"Réponse créative (hors des sentiers battus) à : {message_utilisateur}"

        hypotheses = [h1, h2, h3]
        scores = [self._evaluer(h) for h in hypotheses]

        best_index = scores.index(max(scores))
        meilleure_hypothese = hypotheses[best_index]

        ctx["simulation_hypotheses"] = {
            "hypotheses": hypotheses,
            "scores": scores,
            "choisie": meilleure_hypothese,
            "note_max": max(scores)
        }

        ctx.setdefault("plugins_log", []).append("PluginSimulateurHypotheses : meilleure hypothèse sélectionnée.")
        logger.info(f"[simulateur_hypotheses] Hypothèse choisie : {meilleure_hypothese}")

        return ctx

    def _evaluer(self, reponse: str) -> float:
        # Méthode simple d’évaluation basée sur des critères lexicaux
        score = 0.0
        score += 1.5 if "détaillée" in reponse or "contextuelle" in reponse else 0
        score += 1.2 if "créative" in reponse else 0
        score += 1.0 if "simple" in reponse else 0
        return score
