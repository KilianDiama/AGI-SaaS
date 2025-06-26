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
        if ctx.get("llm_backend") == "openrouter":
            logger.info("🚀 Redirection vers OpenRouter activée")
            from .llm_local import LLM_local
            return await LLM_local().run(ctx)


        return ctx
