"""
Plugin : simulation_hypotheses
Rôle : Générer plusieurs hypothèses de réponse et sélectionner la plus pertinente
Priorité : 3 (avant fusion ou finalisation)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.simulation_hypotheses")

class SimulationHypothesesPlugin(BasePlugin):
    meta = Meta(
        name="simulation_hypotheses",
        priority=3,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base_prompt = ctx.get("user_message") or ctx.get("objectif", {}).get("but", "")

        if not base_prompt:
            ctx["simulation_hypotheses"] = "❌ Aucune base d'hypothèse détectée."
            plugins_log.append("SimulationHypothesesPlugin : rien à simuler")
            return ctx

        # Hypothèses simulées (à remplacer par LLM si disponible)
        hypotheses = [
            f"Je pourrais répondre : '{base_prompt}... d’un point de vue logique.'",
            f"Une autre approche serait : '{base_prompt}... via une analogie personnelle.'",
            f"Ou peut-être : '{base_prompt}... en explorant ses implications émotionnelles.'"
        ]

        scores = [random.uniform(0.4, 1.0) for _ in hypotheses]  # Évaluation simulée
        best_index = scores.index(max(scores))

        ctx["hypotheses"] = hypotheses
        ctx["hypothese_choisie"] = hypotheses[best_index]
        ctx["llm_response"] = hypotheses[best_index]  # La réponse finale sera celle-là

        plugins_log.append("SimulationHypothesesPlugin : hypothèses générées et évaluées")
        logger.info("[simulation_hypotheses] Choix : " + hypotheses[best_index])

        return ctx
