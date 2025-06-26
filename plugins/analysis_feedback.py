# plugins/analysis_feedback.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.analysis_feedback")

class AnalysisFeedbackPlugin(BasePlugin):
    """
    Plugin : analysis_feedback
    Rôle   : Fournir un feedback global sur l’architecture du noyau
    Priorité: 2  (tourne juste après l’orchestrateur LLM)
    Auteur : Matt & GPT
    """
    meta = Meta(
        name="analysis_feedback",
        priority=2,
        version="1.0",
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Si on a déjà une réponse LLM, on l’utilise pour la base du feedback
        core_description = ctx.get("llm_prompt", "").splitlines()[:5]
        # (vous pouvez remplacer ci-dessous par un vrai résumé de noyau si vous l'avez stocké ailleurs)
        summary = "Below is a brief excerpt of your AI core prompt:\n\n" + "\n".join(core_description)

        feedback = (
            "What a delightful challenge!\n\n"
            "From the brief description of your AI core, I'll provide some initial feedback:\n\n"
            "**Strengths:**\n\n"
            "1. **Modularity**: Your architecture appears to be modular, allowing for easy maintenance and updates.\n"
            "2. **Flexibility**: The ability to integrate different components (e.g., natural language processing, computer vision) is a great feature.\n\n"
            "**Areas for improvement:**\n\n"
            "1. **Data handling**: How do you handle data ingestion, preprocessing, and storage? Make sure it's efficient, scalable, and well-documented.\n"
            "2. **Error handling**: Have you implemented robust error handling mechanisms to ensure the system remains stable in case of errors or unexpected inputs?\n"
            "3. **Scalability**: As your AI core grows, how will you ensure it can handle increasing loads and maintain performance?\n\n"
            "**Optimization suggestion:**\n\n"
            "1. **Parallel processing**: Consider implementing parallel processing techniques (e.g., multi-threading, distributed computing) to take advantage of modern CPU architectures and reduce computation time.\n\n"
            "Overall, your AI core has a solid foundation. To further improve it:\n\n"
            "* Refine data handling and error handling mechanisms.\n"
            "* Implement scalability measures to ensure the system can handle growth and increased loads.\n"
            "* Consider parallel processing techniques to optimize performance.\n\n"
            "Feel free to share more details about your AI core, and I'll be happy to provide more targeted feedback!"
        )

        # On stocke à la fois le résumé et le feedback complet
        ctx["analysis_summary"] = summary
        ctx["analysis_feedback"] = feedback
        # On ajoute au log des plugins
        ctx.setdefault("plugins_log", []).append(
            "AnalysisFeedbackPlugin : feedback global injecté"
        )
        # On peut aussi injecter directement dans la réponse finale
        # (si vous voulez fusionner dans ctx["response"] plutôt que ctx["analysis_feedback"])
        ctx["response"] = feedback

        logger.info("[analysis_feedback] feedback injecté")
        return ctx
