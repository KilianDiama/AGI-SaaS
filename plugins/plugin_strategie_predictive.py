# plugins/plugin_strategie_predictive.py

"""
Plugin : strategie_predictive
Rôle   : Anticipe la meilleure configuration de plugins avant d’exécuter le cycle
Priorité : -80 (doit s’exécuter avant le raisonnement)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta
from difflib import SequenceMatcher

logger = logging.getLogger("plugin.strategie_predictive")

class StrategiePredictivePlugin(BasePlugin):
    meta = Meta(
        name="strategie_predictive",
        priority=-80,
        version="1.0",
        author="Toi + GPT"
    )

    # Mémoire simulée : contexte ↔ stratégie ↔ score
    historique = []

    def similarité(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    async def run(self, ctx: Context) -> Context:
        demande = ctx.get("demande_llm", "") or ctx.get("message", "")
        score_max = 0
        meilleure_strategie = None

        # Parcours des cas passés pour trouver un contexte similaire
        for ancien in StrategiePredictivePlugin.historique:
            ancien_ctx = ancien["demande"]
            score = self.similarité(ancien_ctx, demande)
            if score > score_max:
                score_max = score
                meilleure_strategie = ancien["strategie"]

        # Si une stratégie similaire a été trouvée, on la propose
        if meilleure_strategie and score_max > 0.5:
            ctx["strategie_predite"] = meilleure_strategie
            ctx.setdefault("plugins_log", []).append(
                f"StrategiePredictivePlugin : stratégie prédite avec similarité {round(score_max, 2)}"
            )
            logger.info(f"[strategie_predictive] Contexte reconnu → stratégie suggérée : {meilleure_strategie}")

        # Sinon, on mémorise ce nouveau contexte
        StrategiePredictivePlugin.historique.append({
            "demande": demande,
            "strategie": ctx.get("ordre_plugins", [])
        })

        return ctx
