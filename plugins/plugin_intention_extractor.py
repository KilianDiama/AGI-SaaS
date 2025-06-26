# plugins/plugin_intention_extractor.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.intention_extractor")

class PluginIntentionExtractor(BasePlugin):
    meta = Meta(
        name="plugin_intention_extractor",
        priority=1.2,
        version="1.0",
        author="GPT & Toi"
    )

    INTENTION_MAP = {
        "?"         : "question",
        "!"         : "ordre",
        "♥"         : "affectif",
        "😂"        : "humour",
        "…"         : "réflexion",
        "."         : "narration",
        "s'il te plaît": "demande polie",
        "donne"     : "demande",
        "explique"  : "demande",
        "raconte"   : "narration"
    }

    def detect_intention(self, message: str) -> str:
        message = message.lower()
        for key, label in self.INTENTION_MAP.items():
            if key in message:
                return label
        return "générale"

    async def run(self, ctx: Context) -> Context:
        msg = ctx.get("message", "")
        intention = self.detect_intention(msg)

        ctx["intention"] = intention
        ctx.setdefault("plugins_log", []).append(f"plugin_intention_extractor : intention = {intention}")
        logger.info(f"[intention_extractor] → intention détectée : {intention}")

        return ctx
