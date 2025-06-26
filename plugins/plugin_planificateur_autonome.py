""" 
Plugin : planificateur_autonome  
Rôle : Générer un plan structuré en étapes pour atteindre l'objectif donné  
Priorité : 3.9 (juste après perception et stratégie, avant raisonnement)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.planificateur_autonome")

class PlanificateurAutonomePlugin(BasePlugin):
    meta = Meta(
        name="planificateur_autonome",
        priority=3.9,
        version="1.1",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Sécurisation de l'objectif
        objectif_raw = ctx.get("objectif", "")
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", "")).strip()
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw.strip()
        else:
            objectif = str(objectif_raw).strip()

        if not objectif:
            plugins_log.append("PlanificateurAutonomePlugin : 🚫 Aucun objectif à planifier.")
            logger.warning("[planificateur_autonome] Objectif vide ou non valide.")
            return ctx

        plan = [
            f"1. Clarifier l'objectif : « {objectif} »",
            "2. Identifier les ressources nécessaires (données, modules, contexte)",
            "3. Séparer les sous-tâches logiques ou techniques",
            "4. Ordonnancer les sous-tâches dans le temps ou par priorité",
            "5. Prévoir des points de vérification ou de validation intermédiaire",
            "6. Générer une sortie ou une réponse liée à l'étape finale"
        ]

        plan_txt = f"📋 Plan généré pour : {objectif}\n\n" + "\n".join(plan)

        ctx["plan_autonome"] = plan
        if not ctx.get("response"):
            ctx["response"] = plan_txt

        plugins_log.append("PlanificateurAutonomePlugin : ✅ Plan structuré généré.")
        logger.info("[planificateur_autonome] Plan injecté au contexte.")

        return ctx
