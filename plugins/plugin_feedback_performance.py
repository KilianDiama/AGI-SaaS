"""
Plugin : feedback_performance
Rôle : Évaluer la pertinence, la clarté et la cohérence d'une réponse produite
Priorité : 5 (après la génération de réponse)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.feedback_performance")

class FeedbackPerformancePlugin(BasePlugin):
    meta = Meta(
        name="feedback_performance",
        priority=5,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        response = ctx.get("llm_response", "")

        if not response.strip():
            ctx["feedback_performance"] = "🔴 Réponse vide ou absente."
            plugins_log.append("FeedbackPerformancePlugin : réponse vide détectée")
            return ctx

        feedback = []

        # Évaluation basique
        if len(response) < 30:
            feedback.append("🟡 Réponse très courte – pourrait manquer de profondeur.")
        if "je ne sais pas" in response.lower():
            feedback.append("🔴 Contenu non informatif détecté.")
        if response.count("\n") > 10:
            feedback.append("🟡 Réponse potentiellement trop longue ou verbeuse.")
        if response.lower().startswith("oui") or response.lower().startswith("non"):
            feedback.append("🟠 Réponse binaire – vérifier si justifiée.")

        if not feedback:
            feedback.append("🟢 Réponse apparemment claire et pertinente.")

        ctx["feedback_performance"] = "\n".join(feedback)
        plugins_log.append("FeedbackPerformancePlugin : feedback généré")
        logger.info("[feedback_performance] Feedback d'auto-évaluation produit")

        return ctx
