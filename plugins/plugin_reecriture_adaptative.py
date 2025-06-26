""" 
Plugin : reecriture_adaptative  
Rôle : Réécrire la réponse finale pour la rendre plus claire, fluide ou adaptée au contexte  
Priorité : 6.5 (juste après génération brute, avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reecriture_adaptative")

class ReecritureAdaptativePlugin(BasePlugin):
    meta = Meta(
        name="reecriture_adaptative",
        priority=6.5,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("response", "").strip()

        if not reponse:
            plugins_log.append("ReecritureAdaptativePlugin : aucune réponse à réécrire.")
            return ctx

        # Reformulation simple pour démarrer (ex: adoucir ou clarifier)
        if len(reponse) < 30:
            reformulee = f"Voici ce que je peux dire, simplement : {reponse}"
        elif "je ne sais pas" in reponse.lower():
            reformulee = f"Je manque d'informations précises pour répondre pleinement, mais voici ce que je peux proposer : {reponse}"
        else:
            reformulee = f"{reponse}\n\n— Réponse formulée avec soin pour plus de clarté."

        ctx["response_reformulee"] = reformulee
        ctx["response"] = reformulee

        plugins_log.append("ReecritureAdaptativePlugin : réponse reformulée.")
        logger.info("[reecriture_adaptative] Réponse réécrite avec adaptation.")

        return ctx
