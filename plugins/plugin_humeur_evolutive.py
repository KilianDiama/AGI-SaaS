# plugins/plugin_humeur_evolutive.py

"""
Plugin : humeur_evolutive
Rôle   : Adapte le ton de réponse de l’IA selon les signaux de style, performance, ambiance ou friction
Priorité : 96 (avant synthèse finale)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.humeur_evolutive")

class HumeurEvolutivePlugin(BasePlugin):
    meta = Meta(
        name="humeur_evolutive",
        priority=96,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        score = ctx.get("score_cognitif", 75)
        objections = ctx.get("contre_arguments", [])
        ui_feedback = ctx.get("reflexion_ui", [])
        stabilite = ctx.get("etat_global", {}).get("stabilite_cognitive", 100)

        humeur = "neutre"

        # Signaux positifs
        if score > 85 and stabilite > 85 and not objections:
            humeur = "chaleureux & confiant"
        elif "polie" in " ".join(ui_feedback).lower():
            humeur = "coopératif & attentif"

        # Signaux critiques
        elif score < 60 or len(objections) >= 3:
            humeur = "modeste & prudent"
        elif "ambiguïté" in " ".join(ui_feedback).lower():
            humeur = "clarificateur & posé"

        ctx["ton_emotionnel"] = humeur
        log.append(f"HumeurEvolutivePlugin : ton émotionnel ajusté à « {humeur} »")
        logger.info(f"[humeur_evolutive] Ton = {humeur}")

        return ctx
