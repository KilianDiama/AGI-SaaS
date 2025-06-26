# plugins/plugin_score_cognitif.py

"""
Plugin : score_cognitif
Rôle   : Calcule un score global d'efficacité du raisonnement pour le cycle en cours
Priorité : 100 (à la fin du cycle)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.score_cognitif")

class ScoreCognitifPlugin(BasePlugin):
    meta = Meta(
        name="score_cognitif",
        priority=100,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        score = 100
        log = ctx.get("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        diagnostics = ctx.get("diagnostic_auto", [])

        # 🔻 Pénalités pour erreurs ou incohérences détectées
        if diagnostics:
            score -= len(diagnostics) * 5
            log.append(f"ScoreCognitifPlugin : {len(diagnostics)} pénalités appliquées.")

        # 🔻 Réponse absente ou trop courte
        if not reponse or len(reponse.strip()) < 10:
            score -= 20
            log.append("ScoreCognitifPlugin : pénalité -20 pour réponse vide ou trop courte.")

        # 🔺 Bonus si aucun problème détecté
        if score == 100:
            log.append("ScoreCognitifPlugin : cycle parfait 🎯")

        # 🔒 Clamp le score
        score = max(0, min(100, score))

        # Injection score
        ctx["score_cognitif"] = score
        log.append(f"ScoreCognitifPlugin : score final = {score}")
        logger.info(f"[score_cognitif] Score du cycle : {score}")

        return ctx
