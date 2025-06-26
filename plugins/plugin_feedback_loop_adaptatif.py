"""
Plugin : feedback_loop_adaptatif
Rôle : Observer les réponses, critiques et corrections pour apprendre à mieux formuler ses réponses
Priorité : 22
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.feedback_loop_adaptatif")

class FeedbackLoopAdaptatifPlugin(BasePlugin):
    meta = Meta(
        name="feedback_loop_adaptatif",
        priority=22,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        feedback_archive = ctx.setdefault("feedback_archive", [])

        base = {
            "date": datetime.utcnow().isoformat(),
            "input": ctx.get("message", "[inconnu]"),
            "réponse": ctx.get("llm_response", ""),
            "critique": ctx.get("critique_interne", {}).get("commentaire", ""),
            "correction": ctx.get("relecture_poste", {}).get("correction", "")
        }

        feedback_archive.append(base)
        ctx["feedback_archive"] = feedback_archive

        plugins_log.append("FeedbackLoopAdaptatifPlugin : boucle enregistrée")
        logger.info(f"[feedback_loop_adaptatif] Cycle enregistré à {base['date']}")

        return ctx
