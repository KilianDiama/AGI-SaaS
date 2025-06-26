from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.critic_llm")

class PluginCriticLLM(BasePlugin):
    meta = Meta(
        name="plugin_critic_llm",
        version="1.0",
        priority=4.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        try:
            response = ctx.get("llm_response", "").strip()
            if not response:
                ctx.setdefault("plugins_log", []).append("PluginCriticLLM : réponse vide → pas de critique.")
                return ctx

            critique = self.analyse_response(response)
            ctx["critique_llm"] = critique
            ctx.setdefault("plugins_log", []).append("PluginCriticLLM : critique générée.")
            logger.info(f"[critic_llm] Critique :\n{critique}")

        except Exception as e:
            ctx.setdefault("plugins_log", []).append(f"PluginCriticLLM : erreur → {e}")
            logger.warning(f"[critic_llm] Erreur : {e}")

        return ctx

    def analyse_response(self, text: str) -> str:
        feedback = []

        # Clarté et structure
        if len(text.split()) < 15:
            feedback.append("🟠 Réponse trop courte, manque de substance.")
        if not any(p in text for p in ".!?"):
            feedback.append("🟠 Manque de ponctuation forte, le texte peut être perçu comme monotone.")
        if "\n" not in text:
            feedback.append("💡 Ajouter des sauts de ligne pour une meilleure lisibilité.")

        # Pertinence
        if "je ne sais pas" in text.lower():
            feedback.append("🔴 Réponse incertaine : cherche à renforcer la confiance avec un raisonnement.")
        if "erreur" in text.lower():
            feedback.append("❗ Contient une erreur détectée, revoir la source ou le prompt.")

        # Complémentarité
        if "**" not in text and "-" not in text:
            feedback.append("ℹ️ Tu pourrais structurer la réponse avec des listes ou du gras pour guider l’œil.")

        return "\n".join(feedback) if feedback else "✅ Réponse claire, bien structurée et pertinente."

