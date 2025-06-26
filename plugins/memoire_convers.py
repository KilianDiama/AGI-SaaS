# plugins/memoire_convers.py

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.memoire_convers")

class MemoireConversPlugin(BasePlugin):
    meta = Meta(
        name="memoire_convers",
        priority=-997,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        history = ctx.setdefault("history", [])
        payload = ctx.get("payload", {})
        message = payload.get("message", "")
        timestamp = datetime.utcnow().isoformat()

        history.append({
            "from": "user",
            "message": message,
            "timestamp": timestamp
        })

        logger.info(f"[memoire_convers] {len(history)} interactions stockées.")
        ctx.setdefault("plugins_log", []).append("MemoireConversPlugin : message ajouté à l’historique.")
        return ctx
