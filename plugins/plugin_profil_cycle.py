""" 
Plugin : profil_cycle  
Rôle : Générer un profil JSON résumant chaque cycle cognitif pour usage SaaS ou debug avancé  
Priorité : 10 (dernier plugin du cycle)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.profil_cycle")

class ProfilCyclePlugin(BasePlugin):
    meta = Meta(
        name="profil_cycle",
        priority=10,
        version="1.0",
        author="Matthieu & GPT"
    )

    PROFIL_PATH = "data/profils_cycles.json"

    def charger_profils(self):
        if os.path.exists(self.PROFIL_PATH):
            try:
                with open(self.PROFIL_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[profil_cycle] Erreur de lecture : {e}")
        return []

    def sauvegarder_profils(self, profils):
        try:
            with open(self.PROFIL_PATH, "w", encoding="utf-8") as f:
                json.dump(profils, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[profil_cycle] Erreur de sauvegarde : {e}")

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        profils = self.charger_profils()

        profil = {
            "timestamp": datetime.utcnow().isoformat(),
            "objectif": ctx.get("objectif", "Inconnu"),
            "origine_objectif": ctx.get("origine_objectif", "humain"),
            "temps": ctx.get("cycle_duration", "inconnu"),
            "qualité_auto_eval": ctx.get("auto_evaluation", "")[:200],
            "réponse_resume": ctx.get("response", "")[:150]
        }

        profils.append(profil)
        self.sauvegarder_profils(profils)

        logger.info("[profil_cycle] Profil cycle sauvegardé.")
        plugins_log.append("ProfilCyclePlugin : profil résumé du cycle enregistré.")

        return ctx
