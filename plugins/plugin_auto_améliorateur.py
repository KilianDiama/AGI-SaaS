# plugins/plugin_auto_améliorateur.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.auto_améliorateur")

class PluginAutoAmeliorateur(BasePlugin):
    meta = Meta(
        name="plugin_auto_améliorateur",
        version="1.0",
        priority=106.0,  # Après réflexion, juste avant l'export final
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        critique = ctx.get("critique_llm", "")
        response = ctx.get("response", "").strip()

        if not critique or "insuffisante" not in critique.lower():
            ctx.setdefault("plugins_log", []).append("PluginAutoAmeliorateur : réponse jugée OK, pas d’amélioration.")
            return ctx

        prompt = self.build_prompt(critique, response)
        new_response = await self.ask_llm(ctx, prompt)

        if new_response:
            ctx["response"] = new_response
            ctx.setdefault("plugins_log", []).append("PluginAutoAmeliorateur : réponse améliorée automatiquement.")
        else:
            ctx.setdefault("plugins_log", []).append("PluginAutoAmeliorateur : échec tentative d’amélioration.")

        return ctx

    def build_prompt(self, critique: str, texte: str) -> str:
        return (
            f"La critique suivante a été faite sur la réponse :\n"
            f"« {critique} »\n\n"
            f"Améliore cette réponse en conséquence, sans changer son sens :\n"
            f"{texte}"
        )

    async def ask_llm(self, ctx: Context, prompt: str) -> str:
        from plugins.utils.llm_call import call_llm_main
        return await call_llm_main(ctx, prompt)
