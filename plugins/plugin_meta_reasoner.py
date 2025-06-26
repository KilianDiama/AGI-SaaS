# plugins/plugin_meta_reasoner.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.meta_reasoner")

class PluginMetaReasoner(BasePlugin):
    meta = Meta(
        name="plugin_meta_reasoner",
        version="1.0",
        priority=95.0,  # juste avant le loop_manager
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse = ctx.get("response", "").strip()
        if not reponse:
            ctx.setdefault("plugins_log", []).append("PluginMetaReasoner : pas de réponse à analyser.")
            return ctx

        prompt_meta = (
            "Analyse ta réponse suivante comme si tu étais un examinateur critique. "
            "Détecte incohérences, manque de clarté ou d’alignement avec la question. "
            "Indique si la réponse mérite d’être transmise telle quelle ou corrigée.\n\n"
            f"Réponse IA :\n{reponse}\n\nCritique :"
        )

        try:
            from plugins.utils.llm_call import call_llm_main
            critique = await call_llm_main(ctx, prompt_meta)
            ctx["meta_critique"] = critique.strip()
            ctx.setdefault("plugins_log", []).append("PluginMetaReasoner : critique métacognitive injectée.")
        except Exception as e:
            ctx.setdefault("plugins_log", []).append(f"PluginMetaReasoner : erreur analyse → {e}")

        return ctx
