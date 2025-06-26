"""
Plugin : evaluation_utilite
Rôle : Évaluer la clarté, la pertinence et l'utilité perçue de la réponse générée
Priorité : 5 (après réponse mais avant apprentissage)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.evaluation_utilite")

class EvaluationUtilitePlugin(BasePlugin):
    meta = Meta(
        name="evaluation_utilite",
        priority=5,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        response = ctx.get("llm_response", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        score = 0
        remarques = []

        if not response.strip():
            ctx["evaluation_utilite"] = "❌ Pas de réponse à évaluer."
            plugins_log.append("EvaluationUtilitePlugin : vide")
            return ctx

        if objectif and any(word in response.lower() for word in objectif.lower().split()):
            score += 1
            remarques.append("🎯 Réponse en lien direct avec l’objectif.")

        if len(response.strip()) > 100:
            score += 1
            remarques.append("📏 Longueur suffisante pour une explication développée.")

        if "je ne sais pas" not in response.lower():
            score += 1
            remarques.append("✅ Réponse affirmée.")

        if "incompréhensible" in response.lower() or "je suis confus" in response.lower():
            score -= 1
            remarques.append("⚠️ Clarté limitée détectée.")

        conclusion = f"🧠 Score d’utilité : {score}/3\n" + "\n".join(remarques)
        ctx["evaluation_utilite"] = conclusion
        plugins_log.append("EvaluationUtilitePlugin : réponse évaluée")
        logger.info(f"[evaluation_utilite] Score : {score}/3")

        return ctx
