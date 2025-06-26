# plugins/plugin_cycle_long.py

"""
Plugin : cycle_long
Rôle   : Permet à l’IA de conserver des objectifs stratégiques sur plusieurs cycles ou sessions
Priorité : -1 (très tôt)
Auteur  : Toi + GPT
"""

import logging
import time
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cycle_long")

class CycleLongPlugin(BasePlugin):
    meta = Meta(
        name="cycle_long",
        priority=-1,
        version="1.0",
        author="Toi + GPT"
    )

    # Mémoire stratégique partagée (persistante en prod)
    intentions_persistantes = []

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "").strip()

        # Injection des anciennes intentions (résurrection)
        if self.intentions_persistantes:
            ctx.setdefault("intentions_cycle_long", []).extend(self.intentions_persistantes)
            log.append("CycleLongPlugin : objectifs stratégiques restaurés.")

        # Sauvegarde de l’actuel s’il est long
        if objectif and len(objectif) > 25:
            horodatage = int(time.time())
            self.intentions_persistantes.append({
                "objectif": objectif,
                "timestamp": horodatage,
                "cycle_id": ctx.get("cycle_id", "?")
            })
            log.append("CycleLongPlugin : objectif actuel sauvegardé pour suivi long-terme.")

        logger.info(f"[cycle_long] Intentions longues = {len(self.intentions_persistantes)}")
        return ctx
