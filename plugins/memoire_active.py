# plugins/memoire_active.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.memoire_active")


class MemoireActivePlugin(BasePlugin):
    meta = Meta(
        name="memoire_active",
        priority=-996,  # Juste après memoire_convers
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        history = ctx.get("history", [])
        max_len = 5  # ou dynamique selon le type de session

        recent = history[-max_len:]
        resume = "\n".join(f"{h['from']}: {h['message']}" for h in recent)

        ctx["memoire_contextuelle"] = resume
        ctx.setdefault("plugins_log", []).append("MemoireActivePlugin : résumé mémoire injecté.")
        logger.info(f"[memoire_active] Mémoire injectée :\n{resume}")
        return ctx
