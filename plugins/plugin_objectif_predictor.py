# plugins/plugin_objectif_predictor.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.objectif_predictor")

class PluginObjectifPredictor(BasePlugin):
    meta = Meta(
        name="plugin_objectif_predictor",
        version="1.0",
        priority=25.0,  # Avant la planification
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif_actuel = ctx.get("objectif", {}).get("but", "")
        message = ctx.get("user_message", "").strip()

        if objectif_actuel or not message:
            ctx.setdefault("plugins_log", []).append("PluginObjectifPredictor : objectif déjà détecté ou message vide.")
            return ctx

        prompt = self.build_prompt(message)
        predicted_goal = await self.ask_llm(ctx, prompt)

        if predicted_goal:
            ctx["objectif"] = {
                "but": predicted_goal.strip(),
                "état": "à faire",
                "priorité": 1
            }
            ctx.setdefault("plugins_log", []).append(f"PluginObjectifPredictor : objectif prédit → {predicted_goal}")
        else:
            ctx.setdefault("plugins_log", []).append("PluginObjectifPredictor : pas de prédiction.")

        return ctx

    def build_prompt(self, message: str) -> str:
        return (
            f"L'utilisateur a écrit :\n« {message} »\n\n"
            "Quel est probablement son objectif implicite ? "
            "Réponds par une phrase brève décrivant l’objectif sous forme d’action claire (ex : « rédiger une lettre », « corriger un texte », « générer une idée », etc.)."
        )

    async def ask_llm(self, ctx: Context, prompt: str) -> str:
        from plugins.utils.llm_call import call_llm_main
        return await call_llm_main(ctx, prompt)
