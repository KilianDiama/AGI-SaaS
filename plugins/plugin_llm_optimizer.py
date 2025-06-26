import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_optimizer")

class PluginLLMOptimizer(BasePlugin):
    meta = Meta(
        name="plugin_llm_optimizer",
        version="1.0",
        priority=2.2,  # Avant le routeur, après l’analyse
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "générale")
        objectif = ctx.get("objectif", {}).get("but", "")
        user_plan = ctx.get("user", {}).get("plan", "basic")

        # Par défaut
        temperature = 0.7
        max_tokens = 512
        model = "llama3"

        if "code" in intention.lower() or "analyse" in objectif.lower():
            temperature = 0.2
            max_tokens = 1024

        elif "créatif" in intention or "rédaction" in objectif:
            temperature = 0.9
            max_tokens = 1500

        # Plan premium = allongement autorisé
        if user_plan == "illimité":
            max_tokens += 512

        ctx.setdefault("llm_config", {})["temperature"] = temperature
        ctx["llm_config"]["max_tokens"] = max_tokens
        ctx["llm_config"]["model"] = model

        ctx.setdefault("plugins_log", []).append(
            f"PluginLLMOptimizer : config optimisée (temp={temperature}, tokens={max_tokens})"
        )
        logger.info(f"[LLMOptimizer] Configuration : temp={temperature}, tokens={max_tokens}, modèle={model}")
        return ctx
