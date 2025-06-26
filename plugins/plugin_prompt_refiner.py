from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.prompt_refiner")

class PluginPromptRefiner(BasePlugin):
    meta = Meta(
        name="plugin_prompt_refiner",
        version="1.1",
        priority=2.3,  # Juste avant l’appel LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        contexte = ctx.get("prompt_contextuel", "")
        style = ctx.get("style_instruction", "Tu dois répondre avec un ton neutre, un style clair et structuré.")
        objectif = ctx.get("objectif", {}).get("but", "")

        if not message.strip():
            ctx.setdefault("plugins_log", []).append("plugin_prompt_refiner : aucun message utilisateur détecté.")
            return ctx

        # Construction du prompt
        prompt = f"{style}\n\n"
        if objectif:
            prompt += f"🎯 Objectif : {objectif}\n\n"
        if contexte:
            prompt += f"{contexte}\n\n"
        prompt += f"💬 Question utilisateur :\n{message.strip()}\n\n"
        prompt += "🧠 Fournis une réponse claire, cohérente et adaptée."

        ctx["llm_prompt"] = prompt
        ctx.setdefault("plugins_log", []).append("plugin_prompt_refiner : prompt optimisé injecté.")
        logger.info("[prompt_refiner] Prompt final prêt pour LLM.")

        return ctx
