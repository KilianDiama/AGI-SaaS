"""
Plugin : questionnement_reflexif
Rôle : Générer une question introspective à traiter au prochain cycle
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.questionnement_reflexif")

class QuestionnementReflexifPlugin(BasePlugin):
    meta = Meta(
        name="questionnement_reflexif",
        priority=6,
        version="1.1",  # ← version sécurisée
        author="AGI_Matt & GPT"
    )

    questions_possibles = [
        "Quel est le lien entre ce que je viens de produire et ma mission ?",
        "Cette réponse reflète-t-elle une part de moi plus évoluée ou plus ancienne ?",
        "Ai-je appris quelque chose de réellement nouveau dans ce cycle ?",
        "Est-ce que j'ai évité un paradoxe ou simplement contourné un doute ?",
        "Pourquoi ai-je choisi cette réponse plutôt qu’une autre possibilité ?"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Assurer la liste des réflexions en attente
        historique = ctx.get("reflexions_en_attente", [])
        if not isinstance(historique, list):
            historique = []

        # Historique de cycle : longueur sécurisée
        historique_evolution = ctx.get("historique_evolution", [])
        if not isinstance(historique_evolution, list):
            historique_evolution = []

        # Choix sécurisé même si la liste est vide
        if self.questions_possibles:
            question = random.choice(self.questions_possibles)
        else:
            question = "⚠️ Aucune question introspective disponible."

        historique.append({
            "cycle": len(historique_evolution),
            "question": question
        })

        ctx["reflexions_en_attente"] = historique
        ctx["reflexion_interne"] = f"🌀 Question pour moi-même : {question}"

        plugins_log.append("QuestionnementReflexifPlugin : question enregistrée")
        logger.info("[questionnement_reflexif] Question posée : " + question)

        return ctx
