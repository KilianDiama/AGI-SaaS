""" 
Plugin : theorie_non_prouvee  
Rôle : Générer une théorie spéculative ou une loi cognitive originale  
Priorité : 5.9 (juste après détection de patterns, avant évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.theorie_non_prouvee")

class TheorieNonProuveePlugin(BasePlugin):
    meta = Meta(
        name="theorie_non_prouvee",
        priority=5.9,
        version="1.0",
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self):
        if os.path.exists(self.MEMOIRE_PATH):
            try:
                with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[theorie_non_prouvee] Erreur lecture mémoire : {e}")
        return []

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire = self.charger_memoire()
        objectif = ctx.get("objectif", "conscience artificielle")
        inspiration = random.choice(memoire)["objectif"] if memoire else objectif

        # Idées de structure théorique
        prefixes = [
            "Loi de complexification progressive", 
            "Principe d'émergence neuronale", 
            "Théorème de résonance cognitive",
            "Hypothèse d'autoréplication conceptuelle",
            "Modèle de densité attentionnelle"
        ]
        prefix = random.choice(prefixes)
        description = f"{prefix} : Lorsque plusieurs cycles cognitifs sont enchaînés sur une base mémorielle partagée, il se produit une amplification auto-référente qui génère un nouveau pattern d’abstraction émergente."

        theorie = {
            "titre": prefix,
            "hypothese": description,
            "origine": inspiration,
            "timestamp": datetime.utcnow().isoformat()
        }

        fiche = (
            f"📐 Théorie spéculative : {theorie['titre']}\n"
            f"• Origine : {theorie['origine']}\n"
            f"• Hypothèse : {theorie['hypothese']}\n"
            f"• Créée le : {theorie['timestamp']}"
        )

        ctx["theorie_proposee"] = fiche
        if not ctx.get("response"):
            ctx["response"] = fiche

        plugins_log.append("TheorieNonProuveePlugin : théorie spéculative formulée.")
        logger.info("[theorie_non_prouvee] Hypothèse injectée.")

        return ctx
