"""
Plugin : introspection_periodique
Rôle : Auto-analyser périodiquement les réponses passées pour détecter des schémas sous-optimaux
Priorité : 0.9 (avant tout lancement logique)
Auteur : AGI & Matthieu
"""

import logging
import os
import json
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.introspection_periodique")

class IntrospectionPeriodiquePlugin(BasePlugin):
    meta = Meta(
        name="introspection_periodique",
        priority=0.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    HISTO_PATH = "introspection_log.json"
    MAX_LOG = 30
    FREQUENCE = 0.25  # 25 % des runs déclenchent une introspection

    def charger_historique(self):
        if not os.path.exists(self.HISTO_PATH):
            return []
        try:
            with open(self.HISTO_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def sauvegarder(self, historique):
        with open(self.HISTO_PATH, "w", encoding="utf-8") as f:
            json.dump(historique[-self.MAX_LOG:], f, indent=2, ensure_ascii=False)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        reponse = ctx.get("llm_response", "")

        if not message or not reponse:
            plugins_log.append("IntrospectionPeriodiquePlugin : données incomplètes.")
            return ctx

        historique = self.charger_historique()
        historique.append({"message": message, "reponse": reponse})
        self.sauvegarder(historique)

        if random.random() < self.FREQUENCE and len(historique) >= 5:
            # Analyse rudimentaire : vérifier si des réponses reviennent souvent
            comptage = {}
            for h in historique:
                texte = h["reponse"].strip().lower()
                comptage[texte] = comptage.get(texte, 0) + 1

            repetitives = [k for k, v in comptage.items() if v > 2]
            if repetitives:
                ctx["alerte_introspection"] = f"🧠 Plusieurs réponses très répétitives détectées ({len(repetitives)} cas)."
                plugins_log.append("IntrospectionPeriodiquePlugin : schémas répétitifs repérés.")
                logger.warning("[introspection_periodique] Biais répétitif repéré.")
            else:
                plugins_log.append("IntrospectionPeriodiquePlugin : pas de schéma problématique détecté.")

        return ctx
