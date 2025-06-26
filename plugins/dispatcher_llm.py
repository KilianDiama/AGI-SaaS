# plugins/dispatcher_openrouter.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.dispatcher_openrouter")

class DispatcherOpenRouter(BasePlugin):
    meta = Meta(
        name="dispatcher_openrouter",
        priority=150,
        version="1.0",
        author="Toi"
    )

    async def run(self, ctx: Context) -> Context:
        backend = ctx.get("llm_backend")

        if backend == "ollama" or backend == "lmstudio":
            logger.info(f"🚀 Redirection vers moteur local : {backend}")
            from .llm_local import LLMLocalPlugin
            return await LLMLocalPlugin().run(ctx)
        elif backend == "openrouter":
            logger.info("🌐 Redirection vers OpenRouter")
            from .llm_openrouter import OpenRouterLLMPlugin
            return await OpenRouterLLMPlugin().run(ctx)

        return ctx




