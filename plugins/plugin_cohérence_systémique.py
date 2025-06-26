"""
Plugin : coherence_systemique
Rôle : Évaluer l’alignement entre les intentions, la réponse produite, et les états internes
Priorité : 16
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.coherence_systemique")

class CoherenceSystemiquePlugin(BasePlugin):
    meta = Meta(
        name="coherence_systemique",
        priority=16,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        intention = ctx.get("intention_actuelle", "").lower()
        réponse = ctx.get("llm_response", "").lower()
        état = ctx.get("état_interieur", {})
        modules = ctx.get("plugins_log", [])

        score = 100
        alertes = []

        # Check 1 : Intention vs réponse
        if intention and intention not in réponse:
            score -= 25
            alertes.append("Réponse distante de l’intention déclarée.")

        # Check 2 : Ton émotionnel vs intention (si contradiction)
        if "colère" in état.get("ton", "") and "apaiser" in intention:
            score -= 20
            alertes.append("Tension entre émotion interne et intention apaisante.")

        # Check 3 : Logiques contradictoires
        contradiction_detectée = any(
            phrase in réponse for phrase in ["je me contredis", "ce n'est pas logique", "je doute de ce que je dis"]
        )
        if contradiction_detectée:
            score -= 30
            alertes.append("Contradiction explicite détectée dans la réponse.")

        ctx["coherence_score"] = score
        ctx["coherence_alertes"] = alertes
        plugins_log.append(f"CoherenceSystemiquePlugin : score = {score} ({' / '.join(alertes) or 'OK'})")

        if score < 70:
            logger.warning(f"[coherence_systemique] Incohérence modérée à forte (score = {score})")
        else:
            logger.info(f"[coherence_systemique] Alignement global satisfaisant (score = {score})")

        return ctx
