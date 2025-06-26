# plugins/plugin_evolution_guidée.py

"""
Plugin : evolution_guidée
Rôle   : Analyse les stratégies mutées et sélectionne les plus performantes pour les promouvoir
Priorité : 10
Auteur  : Toi + GPT
"""

import logging
from statistics import mean
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.evolution_guidée")

class EvolutionGuidéePlugin(BasePlugin):
    meta = Meta(
        name="evolution_guidée",
        priority=10,
        version="1.0",
        author="Toi + GPT"
    )

    # Mémoire temporaire partagée
    scores_strategies = {}

    async def run(self, ctx: Context) -> Context:
        logs = ctx.get("plugins_log", [])
        strategie_actuelle = tuple(ctx.get("ordre_plugins", []))
        reponse = ctx.get("llm_response", "")

        # Critère de scoring simplifié (ex. : qualité réponse basée sur sa longueur)
        score = len(reponse.strip()) if reponse else 0
        EvolutionGuidéePlugin.scores_strategies[strategie_actuelle] = \
            EvolutionGuidéePlugin.scores_strategies.get(strategie_actuelle, []) + [score]

        moyenne_scores = {
            k: mean(v)
            for k, v in EvolutionGuidéePlugin.scores_strategies.items()
            if len(v) >= 2
        }

        if not moyenne_scores:
            logs.append("EvolutionGuidéePlugin : pas encore assez de données pour sélectionner une stratégie.")
            return ctx

        # Sélection de la meilleure stratégie par score moyen
        meilleure_strat, meilleur_score = max(moyenne_scores.items(), key=lambda x: x[1])
        if tuple(ctx.get("ordre_plugins", [])) != meilleure_strat:
            ctx["strategie_selectionnee"] = list(meilleure_strat)
            logs.append(f"EvolutionGuidéePlugin : stratégie optimale détectée (score moyen = {int(meilleur_score)})")
            logger.info(f"[evolution_guidée] Nouvelle stratégie proposée : {meilleure_strat}")
        else:
            logs.append("EvolutionGuidéePlugin : stratégie actuelle est déjà la meilleure connue.")

        return ctx
