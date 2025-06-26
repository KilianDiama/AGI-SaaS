import logging
from noyau_core import BasePlugin, Context, Meta
from textwrap import wrap

logger = logging.getLogger("plugin.style_enforcer")

class PluginStyleEnforcer(BasePlugin):
    meta = Meta(
        name="plugin_style_enforcer",
        version="1.0",
        priority=4.1,  # Juste après la cohérence, avant la fusion finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        original = ctx.get("llm_response", "")
        style = ctx.get("style_instruction", "neutre, clair et structuré")

        if not original:
            ctx.setdefault("plugins_log", []).append("PluginStyleEnforcer : aucune réponse à améliorer.")
            return ctx

        improved = self.refine_text(original, style)
        ctx["llm_response"] = improved

        ctx.setdefault("plugins_log", []).append("PluginStyleEnforcer : réponse stylisée.")
        logger.info("[StyleEnforcer] Réponse stylisée appliquée.")
        return ctx

    def refine_text(self, text: str, style: str) -> str:
        lines = wrap(text.strip(), 90)
        refined = "\n".join(lines)

        if "neutre" in style.lower():
            refined = refined.replace("!!", ".").replace("...", ".").replace("???", "?")

        if "structuré" in style.lower():
            paragraphs = refined.split("\n\n")
            refined = "\n\n".join(f"🔹 {p.strip()}" for p in paragraphs)

        if "amical" in style.lower():
            refined = refined.replace("Je vais", "Je vais faire de mon mieux pour").replace("vous", "toi")

        return refined.strip()
