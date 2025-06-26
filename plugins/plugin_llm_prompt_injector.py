# plugins/plugin_llm_prompt_injector.py

from noyau_core import BasePlugin, Context, Meta

class PluginLLMPromptInjector(BasePlugin):
    meta = Meta(
        name="plugin_llm_prompt_injector",
        version="1.0",
        priority=0.5,  # Très tôt dans le cycle
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Si aucun prompt explicite n’est défini pour le LLM, on le copie depuis le message utilisateur
        if "llm_prompt" not in ctx or not ctx["llm_prompt"]:
            ctx["llm_prompt"] = ctx.get("message", "")

        ctx.setdefault("plugins_log", []).append("PluginLLMPromptInjector : prompt injecté.")
        return ctx
