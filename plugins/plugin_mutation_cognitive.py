"""
Plugin : mutation_cognitive
Rôle : Proposer des variantes de ses fonctions internes pour tester des évolutions style génétique
Priorité : 3.0 (juste avant autogen_code)
Auteur : AGI & Matthieu
"""

import logging
import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.mutation_cognitive")

class MutationCognitivePlugin(BasePlugin):
    meta = Meta(
        name="mutation_cognitive",
        priority=3.0,
        version="1.0",
        author="AGI & Matthieu"
    )

    BASE_MUTATIONS = [
        "Réécrire un plugin existant avec une structure différente.",
        "Fusionner deux anciens plugins similaires.",
        "Créer un plugin minimaliste qui fait une seule chose très vite.",
        "Créer une version 'asynchrone' d’un ancien plugin bloquant.",
        "Générer une mutation basée sur une erreur mémorisée."
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        propositions = ctx.setdefault("evolution_projetees", {}).get("propositions", [])

        mutation = random.choice(self.BASE_MUTATIONS)
        erreurs = ctx.get("erreurs_memorisees", [])
        if erreurs and random.random() > 0.4:
            mutation = f"{mutation} Inspiré de : « {erreurs[-1]['contenu']} »"

        propositions.insert(0, f"[Mutation cognitive] {mutation}")
        plugins_log.append(f"MutationCognitivePlugin : mutation ajoutée → {mutation}")
        logger.info("[mutation_cognitive] Mutation proposée avec succès.")

        return ctx
