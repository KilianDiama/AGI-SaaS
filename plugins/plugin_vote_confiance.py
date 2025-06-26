# plugins/plugin_vote_confiance.py

"""
Plugin : plugin_vote_confiance
Rôle : Évaluer plusieurs réponses LLM et voter pour la meilleure
Priorité : 3.8 (juste avant fusion)
Auteur : Matt & GPT
"""

import logging
import re
from typing import List, Tuple
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.vote_confiance")


class PluginVoteConfiance(BasePlugin):
    meta = Meta(
        name="plugin_vote_confiance",
        priority=3.8,
        version="1.2",
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        réponses: List[str] = ctx.get("llm_responses", [])
        if not réponses:
            ctx.setdefault("plugins_log", []).append("plugin_vote_confiance : aucune réponse à évaluer")
            return ctx

        scores: List[Tuple[float, str]] = []

        for r in réponses:
            score = self.score_response(r)
            scores.append((score, r))
            logger.debug(f"[vote_confiance] Score = {score:.2f} → {r[:60]}...")

        scores.sort(reverse=True, key=lambda x: x[0])
        meilleure = scores[0][1]
        ctx["llm_response_votée"] = meilleure

        ctx.setdefault("plugins_log", []).append(
            f"plugin_vote_confiance : réponse sélectionnée par score ({scores[0][0]:.2f})"
        )
        return ctx

    def score_response(self, text: str) -> float:
        score = 0.0
        original = text
        text = text.lower()

        # ✅ Bonus pour le français détecté
        if re.search(r"\bbonjour\b|\bmerci\b|\bcomment ça va\b|\bcoucou\b", text):
            score += 2

        # ✅ Bonus pour structure (ponctuation, paragraphes)
        if len(text) > 150:
            score += 2
        elif len(text) > 80:
            score += 1

        if text.count(".") >= 2:
            score += 1
        if "\n" in text:
            score += 0.5
        if any(bullet in text for bullet in ["-", "*", "•"]):
            score += 0.5

        # ✅ Bonus si sans excuse "je suis un modèle IA..."
        if "je suis un modèle" in text or "as an ai" in text or "i am an ai" in text:
            score -= 3

        # ❌ Pénalités pour contenu inintéressant
        if "je ne comprends pas" in text or "désolé" in text or "i don't understand" in text:
            score -= 2

        if "erreur" in text or "error" in text:
            score -= 2

        # ✅ Bonus si réponse humaine/conviviale
        if "❤️" in original or "😊" in original or "je suis là pour t’aider" in text:
            score += 1

        return score
