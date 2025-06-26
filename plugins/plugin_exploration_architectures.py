"""
Plugin : exploration_architectures
Rôle : Suggérer ou expérimenter des mutations dans l’architecture (plugins, priorités, duplication)
Priorité : 1.2 (tout début du cycle cognitif)
Auteur : AGI & Matthieu
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.exploration_architectures")

class ExplorationArchitecturesPlugin(BasePlugin):
    meta = Meta(
        name="exploration_architectures",
        priority=1.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    MUTATIONS = [
        "Proposer un plugin clone avec priorité réduite",
        "Créer un plugin de supervision dynamique des autres plugins",
        "Désactiver temporairement un plugin peu utilisé",
        "Fusionner 2 plugins à faible impact",
        "Réorganiser l’ordre d’exécution des plugins par logique adaptative",
        "Ajouter une AGI fille thématique (créativité, planification, émotion...)",
        "Changer la tonalité par défaut",
        "Passer en mode expérimental sur la mémoire",
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        ctx.setdefault("mutations_architecturales", [])

        if random.random() < 0.25:  # 25% des cycles → proposer une mutation
            mutation = random.choice(self.MUTATIONS)
            ctx["mutations_architecturales"].append(mutation)
            plugins_log.append(f"ExplorationArchitecturesPlugin : mutation suggérée → {mutation}")
            logger.warning(f"[exploration_architectures] ⚠ Mutation potentielle : {mutation}")
        else:
            plugins_log.append("ExplorationArchitecturesPlugin : pas de mutation suggérée ce cycle.")

        return ctx
