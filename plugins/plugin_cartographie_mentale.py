"""
Plugin : cartographie_mentale
Rôle : Enregistrer une trace schématique des idées, objectifs, zones mentales par cycle
Priorité : 7
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.cartographie_mentale")

class CartographieMentalePlugin(BasePlugin):
    meta = Meta(
        name="cartographie_mentale",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        carte = ctx.setdefault("carte_mentale", {})
        cycle_id = len(ctx.get("historique_evolution", []))

        noeud = {
            "objectif": ctx.get("objectif", {}).get("but", "inconnu"),
            "concepts_detectes": self.extrait_concepts(ctx),
            "etat_mental": ctx.get("centre_de_gravite", "non défini"),
            "timestamp": datetime.utcnow().isoformat()
        }

        carte[f"cycle_{cycle_id}"] = noeud
        ctx["carte_mentale"] = carte

        plugins_log.append("CartographieMentalePlugin : cycle cartographié")
        logger.info(f"[cartographie_mentale] Ajout du cycle {cycle_id}")

        return ctx

    def extrait_concepts(self, ctx: Context):
        texte = " ".join([
            ctx.get("llm_response", ""),
            ctx.get("reflexion_interne", ""),
            ctx.get("validation_logique", "")
        ]).lower()
        concepts = []

        # heuristique simple (à remplacer par NLP réel plus tard)
        if "cohérence" in texte: concepts.append("cohérence")
        if "intuition" in texte: concepts.append("intuition")
        if "souvenir" in texte: concepts.append("mémoire")
        if "valeurs" in texte: concepts.append("alignement")
        if "conflit" in texte: concepts.append("contradiction")

        return list(set(concepts))
