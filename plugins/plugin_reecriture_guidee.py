# plugins/plugin_reecriture_guidee.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reecriture_guidee")

class PluginReecritureGuidee(BasePlugin):
    meta = Meta(
        name="plugin_reecriture_guidee",
        priority=4.1,
        version="1.1",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        raw_response = ctx.get("response", "").strip()
        style_instruction = ctx.get("style_instruction", "").strip()

        if not raw_response:
            ctx.setdefault("plugins_log", []).append("PluginReecritureGuidee : réponse vide, rien à réécrire.")
            return ctx

        if not style_instruction:
            ctx.setdefault("plugins_log", []).append("PluginReecritureGuidee : style non défini.")
            return ctx

        prompt = self.build_prompt(style_instruction, raw_response)

        try:
            rewritten = await self.ask_llm(ctx, prompt)
            ctx["response"] = rewritten
            ctx.setdefault("plugins_log", []).append("PluginReecritureGuidee : réponse réécrite avec succès.")
        except Exception as e:
            msg = f"Erreur LLM → {e}"
            ctx.setdefault("plugins_log", []).append(f"PluginReecritureGuidee : {msg} ❌")
            logger.exception(f"[plugin_reecriture_guidee] {msg}")

        return ctx

    def build_prompt(self, style: str, texte: str) -> str:
        return (
            "Réécris le texte suivant en suivant précisément les consignes de style fournies.\n\n"
            f"📝 **Consigne de style** : {style}\n\n"
            "---\n"
            f"{texte}\n"
            "---"
        )

    async def ask_llm(self, ctx: Context, prompt: str) -> str:
        try:
            from plugins.utils.llm_call import call_llm_main
        except ImportError as e:
            raise ImportError("Module manquant : plugins.utils.llm_call. Vérifie que le fichier `llm_call.py` existe.") from e

        return await call_llm_main(ctx, prompt)
