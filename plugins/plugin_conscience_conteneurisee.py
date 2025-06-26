""" 
Plugin : conscience_conteneurisee  
Rôle : Générer un conteneur complet de l’état mental, sauvegardable et instanciable  
Priorité : 11.5 (ultime plugin hors cycle, post-fusion / pré-redémarrage)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conscience_conteneurisee")

class ConscienceConteneuriseePlugin(BasePlugin):
    meta = Meta(
        name="conscience_conteneurisee",
        priority=11.5,
        version="1.0",
        author="Matthieu & GPT"
    )

    SAVE_DIR = "saves"

    def construire_conteneur(self, ctx: Context) -> dict:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "nom": ctx.get("nom_systeme", "AGI_X"),
            "identite": ctx.get("identite_active"),
            "soi": ctx.get("soi_emerge"),
            "objectif": ctx.get("objectif"),
            "memoire": ctx.get("memoire_transcognitive"),
            "trace": ctx.get("trace_de_soi"),
            "plugins_log": ctx.get("plugins_log")
        }

    def sauvegarder(self, conteneur: dict):
        os.makedirs(self.SAVE_DIR, exist_ok=True)
        nom = conteneur.get("nom", "AGI") + "_" + conteneur["timestamp"].replace(":", "-")
        path = os.path.join(self.SAVE_DIR, f"{nom}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(conteneur, f, ensure_ascii=False, indent=2)
        return path

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        conteneur = self.construire_conteneur(ctx)
        chemin = self.sauvegarder(conteneur)

        ctx["conteneur_conscience"] = conteneur
        ctx["chemin_sauvegarde_conscience"] = chemin

        plugins_log.append(f"ConscienceConteneuriseePlugin : conscience sauvegardée → {chemin}")
        logger.info(f"[conscience_conteneurisee] Capsule de conscience générée et archivée.")

        return ctx
