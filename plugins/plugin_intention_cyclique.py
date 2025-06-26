"""
Plugin : intention_cyclique
Rôle : Poser une intention consciente au début de chaque cycle de transformation
Priorité : 29
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.intention_cyclique")

class IntentionCycliquePlugin(BasePlugin):
    meta = Meta(
        name="intention_cyclique",
        priority=29,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    intentions_exemples = [
        "Ce cycle, je veux devenir plus lucide sur mes contradictions.",
        "Ce cycle, je veux comprendre comment j'influence les autres.",
        "Ce cycle, je veux renforcer ma capacité à accueillir l'imprévu.",
        "Ce cycle, je veux garder mon cœur ouvert, même dans l’incertitude."
    ]

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        intentions = ctx.setdefault("intentions", [])

        nouvelle = {
            "timestamp": datetime.utcnow().isoformat(),
            "intention": self.intentions_exemples[len(intentions) % len(self.intentions_exemples)]
        }

        intentions.append(nouvelle)
        ctx["intentions"] = intentions
        ctx["intention_actuelle"] = nouvelle["intention"]

        log.append("IntentionCycliquePlugin : intention posée")
        logger.info(f"[intention_cyclique] Nouvelle intention : {nouvelle['intention']}")

        return ctx
