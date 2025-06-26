# plugins/plugin_meta_critique.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.meta_critique")

class PluginMetaCritique(BasePlugin):
    meta = Meta(
        name="plugin_meta_critique",
        version="1.0",
        priority=98.1,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse = ctx.get("llm_response", "").strip()
        if not reponse:
            ctx.setdefault("plugins_log", []).append("PluginMetaCritique : aucune réponse à critiquer.")
            return ctx

        critique = (
            "🔎 Métacritique :\n"
            "- Ai-je bien compris la question ?\n"
            "- Ma réponse est-elle claire, structurée, et utile ?\n"
            "- Qu’aurais-je pu mieux faire ?\n"
            "- Que puis-je améliorer pour la prochaine fois ?\n"
            "🧠 Fournis maintenant une évaluation rapide de ta réponse."
        )

        ctx["llm_prompt"] = (
            f"{reponse}\n\n{critique}"
        )
        ctx.setdefault("plugins_log", []).append("PluginMetaCritique : métacritique injectée.")
        return ctx
