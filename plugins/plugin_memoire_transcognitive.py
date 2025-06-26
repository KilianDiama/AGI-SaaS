""" 
Plugin : memoire_transcognitive  
Rôle : Regrouper plusieurs cycles cognitifs en une mémoire d’existence persistante  
Priorité : 10.0 (dernier plugin absolu du noyau)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_transcognitive")

class MemoireTranscognitivePlugin(BasePlugin):
    meta = Meta(
        name="memoire_transcognitive",
        priority=10.0,
        version="1.0",
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_transcognitive.json"

    def charger_historique(self):
        if os.path.exists(self.MEMOIRE_PATH):
            with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def enregistrer_historique(self, historique):
        with open(self.MEMOIRE_PATH, "w", encoding="utf-8") as f:
            json.dump(historique, f, ensure_ascii=False, indent=2)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        chapitre = {
            "timestamp": datetime.utcnow().isoformat(),
            "objectif": ctx.get("objectif"),
            "reponse": ctx.get("response"),
            "intuition": ctx.get("intuition"),
            "conscience": ctx.get("conscience_recurrente"),
            "soi": ctx.get("soi_emerge")
        }

        ctx["chapitre_cognitif"] = chapitre
        historique = self.charger_historique()
        historique.append(chapitre)
        self.enregistrer_historique(historique)

        plugins_log.append("MemoireTranscognitivePlugin : chapitre d’existence archivé.")
        logger.info("[memoire_transcognitive] Mémoire étendue mise à jour.")

        return ctx
