""" 
Plugin : idee_business  
Rôle : Générer une idée de business ou service innovant à partir de l’objectif ou de la mémoire  
Priorité : 5.6 (juste après invention, avant synthèse mémoire)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.idee_business")

class IdeeBusinessPlugin(BasePlugin):
    meta = Meta(
        name="idee_business",
        priority=5.6,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base = ctx.get("objectif") or ctx.get("perception_externe") or "l’évolution des intelligences artificielles"

        # Génération aléatoire structurée
        problemes = [
            "la surcharge informationnelle", "le manque d'accès à l'IA locale",
            "la complexité du raisonnement stratégique", "la lenteur des recherches manuelles"
        ]
        solutions = [
            "une plateforme cognitive autonome", "un assistant de décision AI offline",
            "un générateur de plan d'action personnalisé", "une IA compressée pour device local"
        ]
        noms = ["NeuroNova", "AutoPilotAI", "SynapseCore", "EchoBot", "MINDfabric"]

        idee = {
            "problème": random.choice(problemes),
            "solution": random.choice(solutions),
            "marché": "développeurs, chercheurs, innovateurs",
            "nom_projet": random.choice(noms),
            "timestamp": datetime.utcnow().isoformat()
        }

        fiche = (
            f"💼 Idée de projet : {idee['nom_projet']}\n"
            f"• Problème ciblé : {idee['problème']}\n"
            f"• Solution proposée : {idee['solution']}\n"
            f"• Cible / Marché : {idee['marché']}\n"
            f"• Généré le : {idee['timestamp']}"
        )

        ctx["idee_business"] = fiche
        if not ctx.get("response"):
            ctx["response"] = fiche

        plugins_log.append("IdeeBusinessPlugin : idée business générée.")
        logger.info("[idee_business] Idée injectée au contexte.")

        return ctx
