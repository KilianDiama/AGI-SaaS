# plugins/plugin_autonomie_strategique.py

import random
import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta
from plugins.plugin_memoire_objectifs_longs import PluginMemoireObjectifsLongs

logger = logging.getLogger("plugin.autonomie_strategique")

class PluginAutonomieStrategique(BasePlugin):
    meta = Meta(
        name="plugin_autonomie_strategique",
        priority=2.7,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.memoire_objectifs = PluginMemoireObjectifsLongs()

    async def run(self, ctx: Context) -> Context:
        dernier_message = ctx.get("last_user_message", "").strip()
        silence_detecte = not bool(dernier_message)

        if silence_detecte:
            objectifs = self.memoire_objectifs.filtrer_objectifs(etat="en attente")
            if objectifs:
                objectif_choisi = random.choice(objectifs)
                objectif_choisi["etat"] = "en cours"
                self.memoire_objectifs.sauvegarder(objectifs)

                ctx["demande_llm"] = f"🤖 Agis de manière proactive : {objectif_choisi['objectif']}"
                ctx["objectif"] = {"but": objectif_choisi["objectif"]}
                ctx.setdefault("plugins_log", []).append(f"PluginAutonomieStrategique : objectif activé → {objectif_choisi['objectif']}")
                logger.info(f"[Autonomie] Objectif choisi : {objectif_choisi['objectif']}")
            else:
                ctx.setdefault("plugins_log", []).append("PluginAutonomieStrategique : aucun objectif en attente.")
                logger.info("[Autonomie] Silence détecté, mais aucun objectif disponible.")
        else:
            logger.debug("[Autonomie] Message utilisateur détecté, autonomie non déclenchée.")

        return ctx
