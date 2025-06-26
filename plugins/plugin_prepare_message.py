# plugins/plugin_prepare_message.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.prepare_message")

class PluginPrepareMessage(BasePlugin):
    meta = Meta(
        name="plugin_prepare_message",
        version="1.0",
        priority=90,  # 🔁 Exécuté avant generate_actions et llm_openrouter
        author="Matt"
    )

    async def run(self, ctx: Context) -> Context:
        payload = ctx.get("payload", {})
        messages = payload.get("messages", [])

        if messages and isinstance(messages, list):
            # 🔍 Cherche le dernier message utilisateur non vide
            for msg in reversed(messages):
                if msg.get("role") == "user" and msg.get("content"):
                    ctx["message"] = msg["content"]
                    logger.info(f"✅ Message utilisateur injecté dans ctx['message']: {ctx['message']}")
                    break
            else:
                logger.warning("⚠️ Aucun message utilisateur valide trouvé dans messages.")
        else:
            logger.warning("⚠️ Pas de messages valides dans le payload.")

        return ctx
