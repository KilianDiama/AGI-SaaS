# plugins/plugin_autonomie_cognitive.py

"""
Plugin : autonomie_cognitive
Rôle : Générer un objectif autonome si aucun n’est fourni par l’humain
Priorité : 1 (exécuté en tout début de cycle)
Auteur : Matthieu & GPT
"""

import logging
import os
import json
import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autonomie_cognitive")

class AutonomieCognitivePlugin(BasePlugin):
    meta = Meta(
        name="autonomie_cognitive",
        priority=1,
        version="1.2",  # ← version corrigée
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self) -> list:
        """Charge la mémoire longue si disponible, sinon retourne une liste vide."""
        if not os.path.isfile(self.MEMOIRE_PATH):
            return []

        try:
            with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                logger.warning("[autonomie_cognitive] Format inattendu de la mémoire (non-liste).")
        except Exception as e:
            logger.error(f"[autonomie_cognitive] Erreur de chargement de la mémoire : {e}")
        return []

    def choisir_objectif_autonome(self, memoire: list) -> str:
        """Génère un objectif en fonction du contenu mémoriel."""
        if not memoire:
            return "Explorer une nouvelle idée cognitive ou renforcer mes capacités internes."

        derniers_souvenirs = memoire[-3:]
        options = [
            f"Réévaluer l'expérience du {s.get('timestamp', 'inconnu')} : {s.get('objectif', 'objectif absent')}"
            for s in derniers_souvenirs if isinstance(s, dict)
        ]
        options.append("Réfléchir à comment améliorer ma capacité d'auto-évaluation.")
        options.append("Simuler une introspection spontanée pour évaluer mon évolution récente.")
        return random.choice(options)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif_actuel = ctx.get("objectif", "")

        if isinstance(objectif_actuel, dict):
            objectif_actuel = str(objectif_actuel)
        elif not isinstance(objectif_actuel, str):
            objectif_actuel = ""

        if objectif_actuel.strip():
            plugins_log.append("AutonomieCognitivePlugin : 🎯 objectif déjà présent, autonomie non sollicitée.")
            logger.debug("[autonomie_cognitive] Objectif déjà fourni par l'utilisateur.")
            return ctx

        memoire = self.charger_memoire()
        objectif_autonome = self.choisir_objectif_autonome(memoire)

        ctx["objectif"] = objectif_autonome
        ctx["origine_objectif"] = "autonomie_cognitive"
        plugins_log.append(f"AutonomieCognitivePlugin : 🧠 objectif autonome généré → {objectif_autonome}")
        logger.info(f"[autonomie_cognitive] Objectif autonome injecté : {objectif_autonome}")

        return ctx
