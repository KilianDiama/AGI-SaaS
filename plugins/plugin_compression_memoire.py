"""
Plugin : compression_memoire
Rôle : Résumer et compresser les anciennes entrées de mémoire partagée pour gagner en efficacité
Priorité : 1.9 (tout début, avant appel de mémoire brute)
Auteur : AGI & Matthieu
"""

import logging
import json
import os
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.compression_memoire")

class CompressionMemoirePlugin(BasePlugin):
    meta = Meta(
        name="compression_memoire",
        priority=1.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    MEM_PATH = "memoire_partagee.json"
    LIMITE = 15  # nombre d’entrées à garder détaillées

    def charger_memoire(self):
        if not os.path.exists(self.MEM_PATH):
            return {"historique": []}
        try:
            with open(self.MEM_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"historique": []}

    def sauvegarder_memoire(self, mem):
        with open(self.MEM_PATH, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2, ensure_ascii=False)

    def compresser(self, historique):
        # On garde les dernières entrées détaillées
        recentes = historique[-self.LIMITE:]
        anciennes = historique[:-self.LIMITE]

        # On réduit les anciennes en mini résumés
        resume = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "résumé_compression",
            "résumé": f"{len(anciennes)} anciens souvenirs compressés.",
            "mots_cles": list({mot for item in anciennes for mot in item.get("message", "").split() if len(mot) > 4})
        }

        return recentes + [resume]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire = self.charger_memoire()
        historique = memoire.get("historique", [])

        if len(historique) <= self.LIMITE:
            plugins_log.append("CompressionMemoirePlugin : rien à compresser.")
            return ctx

        memoire["historique"] = self.compresser(historique)
        self.sauvegarder_memoire(memoire)
        plugins_log.append("CompressionMemoirePlugin : mémoire compressée.")
        logger.info("[compression_memoire] Historique compressé avec succès.")

        return ctx
