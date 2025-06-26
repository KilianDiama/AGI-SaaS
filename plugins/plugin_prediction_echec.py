# plugins/plugin_prediction_echec.py

"""
Plugin : prediction_echec
Rôle   : Prédit, en amont, si le cycle a de fortes chances de produire un résultat insatisfaisant
Priorité : -20 (avant run LLM)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.prediction_echec")

class PredictionEchecPlugin(BasePlugin):
    meta = Meta(
        name="prediction_echec",
        priority=-20,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        score_precedent = ctx.get("dernier_score", 75)
        objectif = ctx.get("objectif_general", "")
        plugins = ctx.get("ordre_plugins", [])
        message = ctx.get("message", "").lower()
        risques = []

        # Risque 1 : objectif absent ou trop vague
        if not objectif or len(objectif.strip()) < 10:
            risques.append("Objectif mal défini.")

        # Risque 2 : plugins incompatibles (ex. deux LLM simultanés)
        llm_plugins = [p for p in plugins if "llm" in p]
        if len(llm_plugins) > 1:
            risques.append(f"Conflit possible entre {llm_plugins}.")

        # Risque 3 : surcharge de contexte ou profondeur excessive
        if len(ctx.get("messages", [])) > 15:
            risques.append("Contexte trop lourd : surcharge probable.")

        # Risque 4 : tendances récentes à l’échec
        if score_precedent < 60:
            risques.append("Cycles récents peu efficaces.")

        # Risque 5 : demande incohérente ou contradictoire
        if any(mot in message for mot in ["blabla", "triche", "juste test"]):
            risques.append("Demande potentiellement non sérieuse.")

        # Injecter la prédiction dans le contexte
        if risques:
            ctx["risque_echec"] = {
                "niveau": "élevé" if len(risques) >= 3 else "modéré",
                "causes": risques
            }
            log.append(f"PredictionEchecPlugin : échec anticipé ({len(risques)} causes)")
            logger.warning(f"[prediction_echec] Risques détectés : {risques}")
        else:
            log.append("PredictionEchecPlugin : aucun risque détecté.")
            logger.info("[prediction_echec] Cycle jugé sain.")

        return ctx
