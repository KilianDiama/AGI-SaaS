"""
Plugin : memoire_long_terme_adaptative
Rôle : Retenir les préférences, faits importants et sujets récurrents pour les réinjecter automatiquement
Priorité : 1.4 (début du cycle)
Auteur : AGI & Matthieu
"""

import logging
import os
import json
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_long_terme_adaptative")

class MemoireLongTermeAdaptativePlugin(BasePlugin):
    meta = Meta(
        name="memoire_long_terme_adaptative",
        priority=1.4,
        version="1.0",
        author="AGI & Matthieu"
    )

    MEMOIRE_PATH = "memoire_long_terme.json"

    def charger_memoire(self):
        if not os.path.exists(self.MEMOIRE_PATH):
            return {}
        try:
            with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    def sauvegarder_memoire(self, memoire):
        with open(self.MEMOIRE_PATH, "w", encoding="utf-8") as f:
            json.dump(memoire, f, indent=2, ensure_ascii=False)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()
        memoire = self.charger_memoire()
        sujets = memoire.get("sujets", {})

        # Injection si sujet déjà connu
        for mot_cle, valeur in sujets.items():
            if mot_cle in message:
                ctx.setdefault("memoire_reinjectee", []).append(f"{mot_cle} → {valeur}")
                plugins_log.append(f"MemoireLongTermeAdaptativePlugin : réinjection → {mot_cle}")
                logger.info(f"[memoire_long_terme] Sujet reconnu : {mot_cle}")
                break

        # Extraction naïve pour apprentissage
        if "je suis ton créateur" in message or "je m'appelle" in message:
            info = message.split("je ")[1]
            sujets["createur"] = info
            memoire["sujets"] = sujets
            self.sauvegarder_memoire(memoire)
            plugins_log.append("MemoireLongTermeAdaptativePlugin : nouvelle donnée retenue.")
            logger.info(f"[memoire_long_terme] Apprentissage d’une nouvelle info : {info}")

        return ctx
