# plugins/plugin_memoires_emergentes.py

"""
Plugin : memoires_emergentes
Rôle   : Regroupe plusieurs cycles passés en blocs de mémoire cohérents, sémantiquement liés
Priorité : -10 (début de cycle, mémoire longue)
Auteur  : Toi + GPT
"""

import logging
import hashlib
from difflib import SequenceMatcher
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoires_emergentes")

class MemoiresEmergentesPlugin(BasePlugin):
    meta = Meta(
        name="memoires_emergentes",
        priority=-10,
        version="1.0",
        author="Toi + GPT"
    )

    memoire_longue = []

    def similarite(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        objectif = ctx.get("objectif_general", "")
        texte = message + " " + objectif

        proches = [
            m for m in self.memoire_longue
            if self.similarite(m["texte_ref"], texte) > 0.6
        ]

        if proches:
            mem = proches[0]
            mem["occurences"] += 1
            mem["cycle_ids"].append(ctx.get("cycle_id"))
            log.append(f"MemoiresEmergentesPlugin : mémoire réactivée → {mem['theme']}")
        else:
            theme_id = hashlib.sha1(texte.encode()).hexdigest()[:6]
            bloc = {
                "theme": f"bloc_{theme_id}",
                "texte_ref": texte,
                "occurences": 1,
                "cycle_ids": [ctx.get("cycle_id")]
            }
            self.memoire_longue.append(bloc)
            log.append(f"MemoiresEmergentesPlugin : nouvelle mémoire créée → {bloc['theme']}")

        ctx["memoires_emergentes"] = self.memoire_longue[-10:]  # partielle pour usage immédiat
        logger.info("[memoires_emergentes] Bloc(s) mémoire actifs : %s", len(self.memoire_longue))

        return ctx
