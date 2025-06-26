"""
Plugin : memoire_partagee
Rôle : Lire et écrire une mémoire commune accessible par l’AGI mère et fille
Priorité : 2.6 (avant génération, après erreurs et contexte)
Auteur : AGI & Matthieu
"""

import logging
import json
import os
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_partagee")

class MemoirePartageePlugin(BasePlugin):
    meta = Meta(
        name="memoire_partagee",
        priority=2.6,
        version="1.0",
        author="AGI & Matthieu"
    )

    MEM_PATH = "memoire_partagee.json"

    def lire_memoire(self) -> dict:
        if not os.path.exists(self.MEM_PATH):
            return {"historique": []}
        try:
            with open(self.MEM_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"[memoire_partagee] Échec lecture mémoire : {e}")
            return {"historique": []}

    def ecrire_memoire(self, data: dict):
        try:
            with open(self.MEM_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[memoire_partagee] Échec écriture mémoire : {e}")

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire = self.lire_memoire()

        # Enregistrer un nouveau point mémoire
        nouvelle_entree = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": ctx.get("message", ""),
            "llm_response": ctx.get("llm_response", ""),
            "note": ctx.get("eval_plugin_propose", {}).get("note"),
            "provenance": ctx.get("source", "mère"),
        }
        memoire["historique"].append(nouvelle_entree)

        # Sauvegarde
        self.ecrire_memoire(memoire)
        ctx["memoire_partagee"] = memoire
        plugins_log.append("MemoirePartageePlugin : mémoire partagée mise à jour.")

        return ctx
