"""
Plugin : vote_lli
Rôle : Voter entre plusieurs réponses concurrentes issues de LLM ou sous-AGI
Priorité : 3.8 (après réception des réponses mais avant fusion)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta
from collections import Counter

logger = logging.getLogger("plugin.vote_lli")

class VoteLLIPlugin(BasePlugin):
    meta = Meta(
        name="vote_lli",
        priority=3.8,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponses = ctx.get("llm_responses", [])
        scores = Counter()

        if not reponses or len(reponses) < 2:
            return ctx  # Rien à voter

        for i, rep in enumerate(reponses):
            score = 0
            rep = rep.strip().lower()
            if any(mot in rep for mot in ["logique", "cohérent", "clair", "structuré"]):
                score += 2
            if "je ne sais pas" in rep or "pas sûr" in rep:
                score -= 1
            if len(rep) > 150:
                score += 1
            if len(rep) < 30:
                score -= 1
            scores[i] = score

        if scores:
            meilleur = scores.most_common(1)[0][0]
            ctx["llm_response"] = reponses[meilleur]
            plugins_log.append(f"VoteLLIPlugin : réponse #{meilleur+1} sélectionnée par vote pondéré")
            logger.info(f"[vote_lli] Réponse #{meilleur+1} choisie sur {len(reponses)}.")

        return ctx
