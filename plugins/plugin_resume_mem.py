# plugins/memoire/plugin_resume_mem.py

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.resume_mem")

class ResumeMemoirePlugin(BasePlugin):
    meta = Meta(
        name="resume_mem",
        priority=-979,  # juste après memoire_long_terme
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        history = ctx.get("history", [])
        if len(history) < 10:
            return ctx  # pas assez long pour résumer

        # Construction simple du résumé
        messages = [h["message"] for h in history[-10:]]
        resume = "Résumé des 10 derniers échanges :\n" + "\n".join(f"- {m}" for m in messages)

        cle = f"résumé_{datetime.utcnow().isoformat()}"
        ctx["memoire_action"] = "write"
        ctx["memoire_cle"] = cle
        ctx["memoire_valeur"] = resume
        ctx["memoire_tags"] = ["résumé", "conversation", "auto"]

        ctx.setdefault("plugins_log", []).append(f"ResumeMemoirePlugin : résumé sauvegardé sous {cle}")
        logger.info(f"[resume_mem] Résumé ajouté à la mémoire long terme.")
        return ctx
