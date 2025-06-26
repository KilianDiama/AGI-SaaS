# plugins/plugin_reponse_multimodale.py

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.reponse_multimodale")

class PluginReponseMultimodale(BasePlugin):
    meta = Meta(
        name="plugin_reponse_multimodale",
        version="1.0",
        priority=3.2,  # Après génération initiale, avant résolution finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        if "llm_responses" not in ctx or not ctx["llm_responses"]:
            ctx.setdefault("plugins_log", []).append("PluginReponseMultimodale : aucune réponse à comparer.")
            return ctx

        responses = ctx["llm_responses"]
        scored_responses = []

        for response in responses:
            score = self.evaluate_response_quality(response)
            scored_responses.append((response, score))

        # Trier et choisir la meilleure
        best_response, best_score = max(scored_responses, key=lambda x: x[1])
        ctx["llm_response_votée"] = best_response
        ctx["evaluation_reponse"] = {
            "verdict": "choisie via vote",
            "note": best_score,
            "longueur": len(best_response)
        }

        ctx.setdefault("plugins_log", []).append("PluginReponseMultimodale : meilleure réponse sélectionnée.")
        logger.info(f"[reponse_multimodale] Score max = {best_score:.2f}")

        return ctx

    def evaluate_response_quality(self, response: str) -> float:
        # Heuristique simple : long = informatif, clair = peu de "?" ou de vide
        length = len(response.strip())
        penalite = response.count("?") * 2
        if "Exception" in response or not response.strip():
            return 0
        return max((length - penalite) / 100.0, 0.1)
