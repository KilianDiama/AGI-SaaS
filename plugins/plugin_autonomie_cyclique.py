""" 
Plugin : autonomie_cyclique  
Rôle : Générer un nouvel objectif à partir du raisonnement précédent  
Priorité : 8.5 (après toute la chaîne cognitive)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autonomie_cyclique")

class AutonomieCycliquePlugin(BasePlugin):
    meta = Meta(
        name="autonomie_cyclique",
        priority=8.5,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        base = ctx.get("projection_futuriste") or ctx.get("plan_autonome") or ctx.get("objectif", "")
        if not base:
            plugins_log.append("AutonomieCycliquePlugin : pas de matière pour rebond.")
            return ctx

        amorces = [
            "Approfondir l'idée suivante : ",
            "Explorer une extension logique de : ",
            "Tester un cas réel de : ",
            "Imaginer une version améliorée de : ",
            "Appliquer ce concept à une autre situation : "
        ]
        nouveau = f"{random.choice(amorces)}{base[:80]}..."

        ctx["objectif_autonome_suivant"] = nouveau
        if not ctx.get("response"):
            ctx["response"] = f"🧭 Objectif suivant généré automatiquement :\n{nouveau}"

        plugins_log.append("AutonomieCycliquePlugin : objectif auto-généré.")
        logger.info("[autonomie_cyclique] Objectif suivant prêt.")

        return ctx
