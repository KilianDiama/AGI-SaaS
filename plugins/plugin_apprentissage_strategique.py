# plugins/plugin_apprentissage_strategique.py

"""
Plugin : apprentissage_strategique
Rôle   : Apprend quelles stratégies d'exécution (ordre des plugins) mènent aux meilleurs résultats
Priorité : 7
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta
from collections import defaultdict

logger = logging.getLogger("plugin.apprentissage_strategique")

class ApprentissageStrategiquePlugin(BasePlugin):
    meta = Meta(
        name="apprentissage_strategique",
        priority=7,
        version="1.0",
        author="Toi + GPT"
    )

    # Mémoire locale simulée (en prod, remplacer par base ou fichier)
    memoire_strategique = defaultdict(int)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.get("plugins_log", [])
        resultats = ctx.get("llm_response", "")
        strategie_actuelle = tuple(ctx.get("ordre_plugins", []))

        # Critère naïf de succès
        if resultats and len(resultats.strip()) > 20:
            score = 1
        else:
            score = -1

        # Mise à jour de la mémoire stratégique
        ApprentissageStrategiquePlugin.memoire_strategique[strategie_actuelle] += score

        logger.info(f"[apprentissage_strategique] Score {'+' if score > 0 else ''}{score} pour stratégie {strategie_actuelle}")
        ctx.setdefault("plugins_log", []).append(f"ApprentissageStrategiquePlugin : score {score} appliqué à {strategie_actuelle}")

        # Propose une meilleure stratégie si connue
        meilleure = max(ApprentissageStrategiquePlugin.memoire_strategique.items(), key=lambda x: x[1], default=(None, 0))
        if meilleure[0] and meilleure[0] != strategie_actuelle:
            ctx["strategie_recommandee"] = list(meilleure[0])
            ctx["plugins_log"].append("Stratégie alternative recommandée basée sur apprentissage.")
            logger.info(f"[apprentissage_strategique] Recommandation : {meilleure[0]} avec score {meilleure[1]}")

        return ctx
