# plugins/input_plugin.py
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.input")

class InputPlugin(BasePlugin):
    meta = Meta(
        name="input_plugin",
        version="1.0",
        priority=-101,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Si le POST a mis les messages sous payload["messages"], on les expose directement
        payload = ctx.get("payload", {})
        if "messages" in payload:
            ctx["messages"] = payload["messages"]
            logger.info(f"[input_plugin] Injecté {len(ctx['messages'])} messages dans ctx")
        return ctx
