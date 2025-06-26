# plugins/plugin_reflexion_transversale.py

"""
Plugin : reflexion_transversale
Rôle   : Analyse les cycles passés pour détecter des patterns d'efficacité ou d'échec
Priorité : 101 (après score_cognitif)
Auteur  : Toi + GPT
"""

import logging
from statistics import mean
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reflexion_transversale")

class ReflexionTransversalePlugin(BasePlugin):
    meta = Meta(
        name="reflexion_transversale",
        priority=101,
        version="1.0",
        author="Toi + GPT"
    )

    # Mémoire interne simulée
    historique = []

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        score = ctx.get("score_cognitif", 0)
        strat = tuple(ctx.get("ordre_plugins", []))

        # Ajout à l'historique
        ReflexionTransversalePlugin.historique.append({
            "strategie": strat,
            "score": score,
            "id": ctx.get("cycle_id")
        })

        # Analyse sur les 5 derniers cycles
        recent = ReflexionTransversalePlugin.historique[-5:]
        moyenne = mean([c["score"] for c in recent]) if recent else 0

        if moyenne < 60:
            log.append("ReflexionTransversalePlugin : tendance globale faible détectée.")
            ctx["reflexion_globale"] = "baisse d'efficacité cognitive"

        elif moyenne > 85:
            log.append("ReflexionTransversalePlugin : tendance globalement optimale.")
            ctx["reflexion_globale"] = "cycle stable et performant"

        else:
            log.append("ReflexionTransversalePlugin : performance moyenne stable.")
            ctx["reflexion_globale"] = "performance modérée"

        logger.info(f"[reflexion_transversale] Moyenne des 5 derniers scores : {round(moyenne,1)}")
        return ctx
