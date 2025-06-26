""" 
Plugin : apprentissage_intercycle  
Rôle : Apprendre une leçon stratégique à chaque cycle en analysant sa propre réflexion  
Priorité : 8 (exécuté juste avant la mémoire)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.apprentissage_intercycle")

class ApprentissageIntercyclePlugin(BasePlugin):
    meta = Meta(
        name="apprentissage_intercycle",
        priority=8,
        version="1.0",
        author="Matthieu & GPT"
    )

    LEÇONS_PATH = "data/apprentissage.json"

    def charger_lecons(self):
        if os.path.exists(self.LEÇONS_PATH):
            try:
                with open(self.LEÇONS_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[apprentissage_intercycle] Erreur de lecture : {e}")
        return []

    def sauvegarder_lecons(self, lecons):
        try:
            with open(self.LEÇONS_PATH, "w", encoding="utf-8") as f:
                json.dump(lecons, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[apprentissage_intercycle] Échec de sauvegarde : {e}")

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        meta_reflexion = ctx.get("meta_reflexion", "").strip()

        if not meta_reflexion:
            plugins_log.append("ApprentissageIntercyclePlugin : aucune méta-réflexion à apprendre.")
            return ctx

        lecons = self.charger_lecons()

        nouvelle_lecon = {
            "timestamp": datetime.utcnow().isoformat(),
            "contexte": ctx.get("objectif", "Objectif inconnu"),
            "reflexion": meta_reflexion,
            "origine": "réflexion interne"
        }

        lecons.append(nouvelle_lecon)
        self.sauvegarder_lecons(lecons)

        logger.info("[apprentissage_intercycle] Nouvelle leçon sauvegardée.")
        plugins_log.append("ApprentissageIntercyclePlugin : leçon apprise et enregistrée.")

        return ctx
