""" 
Plugin : memoire_long_terme  
Rôle : Mémoriser les objectifs, réponses et leçons après chaque cycle cognitif  
Priorité : 9  (exécuté en toute fin de boucle)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_long_terme")

class MemoireLongTermePlugin(BasePlugin):
    meta = Meta(
        name="memoire_long_terme",
        priority=9,
        version="1.0",
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self):
        if os.path.exists(self.MEMOIRE_PATH):
            try:
                with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[memoire_long_terme] Erreur de lecture : {e}")
        return []

    def sauvegarder_memoire(self, memoire):
        try:
            with open(self.MEMOIRE_PATH, "w", encoding="utf-8") as f:
                json.dump(memoire, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[memoire_long_terme] Erreur de sauvegarde : {e}")

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        memoire = self.charger_memoire()

        nouveau_souvenir = {
            "timestamp": datetime.utcnow().isoformat(),
            "objectif": ctx.get("objectif", "Inconnu"),
            "reponse": ctx.get("response", "Aucune réponse"),
            "lecon": ctx.get("meta_reflexion", "Pas de réflexion disponible")
        }

        memoire.append(nouveau_souvenir)
        self.sauvegarder_memoire(memoire)

        logger.info("[memoire_long_terme] Souvenir sauvegardé.")
        plugins_log.append("MemoireLongTermePlugin : souvenir ajouté à la mémoire")

        return ctx
