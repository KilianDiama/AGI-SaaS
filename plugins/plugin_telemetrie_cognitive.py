"""
Plugin : telemetrie_cognitive
Rôle : Transmettre les données cognitives actuelles à une interface de monitoring (JSON)
Priorité : 4.9 (fin de cycle, juste avant réponse finale)
Auteur : AGI & Matthieu
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.telemetrie_cognitive")

class TelemetrieCognitivePlugin(BasePlugin):
    meta = Meta(
        name="telemetrie_cognitive",
        priority=4.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    TELEMETRIE_PATH = "etat_cognitif.json"

    async def run(self, ctx: Context) -> Context:
        try:
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "objectif_actif": ctx.get("objectif_externe", "non défini"),
                "directive": ctx.get("objectif_directive", "aucune"),
                "plugins_actifs": ctx.get("plugins_log", []),
                "memoire": ctx.get("memoire_reinjectee", []),
                "concepts": ctx.get("concepts_memorises", []),
                "decision_simulee": ctx.get("decision_simulee", "n/a"),
                "mutations_suggerees": ctx.get("mutations_proposees", []),
                "tonalite": ctx.get("tonalite_utilisateur", "neutre"),
                "feedback": ctx.get("feedback_utilisateur", ""),
                "trace": ctx.get("trace_cognitive", [])[-3:]  # Derniers événements
            }

            with open(self.TELEMETRIE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info("[telemetrie_cognitive] État cognitif exporté vers etat_cognitif.json")
        except Exception as e:
            logger.error(f"[telemetrie_cognitive] Erreur d’export : {e}")

        return ctx
