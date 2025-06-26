""" 
Plugin : anticipation_recurrente  
Rôle : Anticiper les prochaines requêtes ou cycles potentiels à partir de l’objectif actuel  
Priorité : 4.5 (après fusion, avant évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.anticipation_recurrente")

class AnticipationRecurrentePlugin(BasePlugin):
    meta = Meta(
        name="anticipation_recurrente",
        priority=4.5,
        version="1.1",  # ← version corrigée
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Sécurisation de l’objectif
        objectif_raw = ctx.get("objectif", "")
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", ""))
        else:
            objectif = str(objectif_raw)

        # Sécurisation de la réponse
        reponse_raw = ctx.get("response", "")
        reponse = str(reponse_raw)

        objectif = objectif.strip()
        reponse = reponse.strip()

        if not objectif or not reponse:
            plugins_log.append("AnticipationRecurrentePlugin : ❌ anticipation impossible (objectif ou réponse vide).")
            logger.warning("[anticipation_recurrente] Objectif ou réponse non valides.")
            return ctx

        # Propositions d’anticipation
        suite_possible = [
            "Souhaiteras-tu que je vérifie la validité de cette réponse ?",
            "Dois-je explorer une alternative stratégique à ce que je viens de proposer ?",
            "Souhaites-tu que je résume ou structure cela en plan d’action ?",
            "Devrais-je enregistrer ce schéma comme modèle de réflexion pour plus tard ?"
        ]

        anticipation = random.choice(suite_possible)
        plan = [
            "1. Analyser la réponse produite.",
            "2. Proposer une suite logique ou complémentaire.",
            "3. Se préparer à une boucle de suivi autonome."
        ]

        ctx["anticipation_next"] = anticipation
        ctx["anticipation_plan"] = plan
        plugins_log.append("AnticipationRecurrentePlugin : ✅ anticipation projetée.")
        logger.info(f"[anticipation_recurrente] Anticipation injectée : {anticipation}")

        return ctx
