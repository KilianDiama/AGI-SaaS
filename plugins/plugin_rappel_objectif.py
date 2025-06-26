from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.rappel_objectif")

class PluginRappelObjectif(BasePlugin):
    meta = Meta(
        name="plugin_rappel_objectif",
        version="1.0",
        priority=2.6,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historiques = ctx.get("objectifs_mémorisés", [])
        objectif_actuel = ctx.get("objectif", {}).get("but", "").lower()

        if not historiques or objectif_actuel in ["", "répondre à une question générale"]:
            logger.debug("[rappel_objectif] Rien à rappeler.")
            return ctx

        # Choix simple du dernier objectif pertinent
        dernier = sorted(historiques, key=lambda o: o["timestamp"], reverse=True)[0]
        rappel = f"🎯 Rappel de ton objectif : « {dernier['but']} »"

        ctx["objectif_rappelé"] = rappel
        ctx.setdefault("plugins_log", []).append("PluginRappelObjectif : objectif rappelé injecté.")
        logger.info(f"[rappel_objectif] Objectif rappelé : {dernier['but']}")
        return ctx
