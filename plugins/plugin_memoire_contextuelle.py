"""
Plugin : memoire_contextuelle
Rôle : Injecter dans le contexte les souvenirs pertinents (anciens messages similaires)
Priorité : 1.8 (après compression, avant toute génération)
Auteur : AGI & Matthieu
"""

import logging
import json
import os
from difflib import SequenceMatcher
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_contextuelle")

class MemoireContextuellePlugin(BasePlugin):
    meta = Meta(
        name="memoire_contextuelle",
        priority=1.8,
        version="1.0",
        author="AGI & Matthieu"
    )

    MEM_PATH = "memoire_partagee.json"
    SEUIL = 0.35  # seuil de similarité pour souvenir pertinent
    MAX = 3       # nombre max de souvenirs à injecter

    def charger_memoire(self):
        if not os.path.exists(self.MEM_PATH):
            return []
        try:
            with open(self.MEM_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("historique", [])
        except:
            return []

    def similarite(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        if not message:
            plugins_log.append("MemoireContextuellePlugin : message vide → rien à lier.")
            return ctx

        souvenirs = self.charger_memoire()
        scores = [
            {"score": self.similarite(message, s.get("message", "")), "souvenir": s}
            for s in souvenirs if s.get("message")
        ]

        proches = sorted([s for s in scores if s["score"] >= self.SEUIL], key=lambda x: -x["score"])[:self.MAX]

        if proches:
            extraits = [f"Souvenir ({int(p['score']*100)}%) : {p['souvenir']['message']}" for p in proches]
            ctx["contexte_annexe"] = "\n".join(extraits)
            plugins_log.append(f"MemoireContextuellePlugin : {len(proches)} souvenirs injectés au contexte.")
            logger.info(f"[memoire_contextuelle] {len(proches)} anciens messages ajoutés au contexte.")
        else:
            plugins_log.append("MemoireContextuellePlugin : aucun souvenir pertinent trouvé.")

        return ctx
