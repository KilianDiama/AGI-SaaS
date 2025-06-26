# plugins/plugin_feedback_iteratif.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.feedback_iteratif")

class PluginFeedbackIteratif(BasePlugin):
    meta = Meta(
        name="plugin_feedback_iteratif",
        version="1.0",
        priority=3.5,  # Après réponse votée, avant envoi final
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response_votée") or ctx.get("llm_response", "")
        if not response.strip():
            ctx.setdefault("plugins_log", []).append("PluginFeedbackIteratif : réponse vide, rien à améliorer.")
            return ctx

        # Crée une invite d'auto-révision
        prompt = (
            "Améliore cette réponse en termes de clarté, structure, fluidité et humanité. "
            "Corrige si besoin, mais conserve le sens original.\n\n"
            "---\n"
            f"{response.strip()}\n"
            "---"
        )

        # Simulation d'une amélioration (à connecter à un LLM local si besoin)
        improved = await self.fake_llm_refine(prompt)

        ctx["llm_response"] = improved
        ctx.setdefault("plugins_log", []).append("PluginFeedbackIteratif : réponse améliorée par itération.")
        logger.info(f"[feedback_iteratif] Réponse finale améliorée injectée.")

        return ctx

    async def fake_llm_refine(self, prompt: str) -> str:
        # 👉 À remplacer par un vrai appel LLM si disponible
        return prompt.replace("---", "").replace("Améliore cette réponse", "[Amélioration automatique]")

