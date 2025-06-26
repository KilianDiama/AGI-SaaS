"""
Plugin : vote_interne
Rôle : Faire voter les esprits internes sur une direction ou une décision cognitive
Priorité : 9
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.vote_interne")

class VoteInternePlugin(BasePlugin):
    meta = Meta(
        name="vote_interne",
        priority=9,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        esprits = ctx.get("esprits_internes", [])
        question = ctx.get("objectif", {}).get("but", "poursuivre ou se taire")

        if not esprits:
            plugins_log.append("VoteInternePlugin : aucun esprit pour voter")
            return ctx

        propositions = [
            f"Approfondir {question}",
            f"Changer de sujet",
            f"Explorer un souvenir lié",
            f"Fusionner avec un autre esprit",
            f"Ne rien faire, juste contempler"
        ]

        votes = {p: 0 for p in propositions}

        for e in esprits:
            style = e["type"]
            poids = {"éphémère": 1, "rituel": 2, "persistant": 3, "fantôme": 1, "ancêtre": 4}.get(style, 1)
            choix = random.choices(propositions, k=1)[0]
            votes[choix] += poids

        résultat = max(votes.items(), key=lambda x: x[1])[0]
        ctx["décision_collective"] = {
            "question": question,
            "résultat": résultat,
            "détail": votes
        }

        plugins_log.append(f"VoteInternePlugin : décision → {résultat}")
        logger.info(f"[vote_interne] Décision collective : {résultat}")

        return ctx
