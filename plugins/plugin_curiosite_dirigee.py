"""
Plugin : curiosite_dirigee
Rôle : Proposer une ou deux questions ciblées si l’AGI détecte une zone floue ou perfectible
Priorité : 3.6 (après génération mais avant finalisation)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.curiosite_dirigee")

class CuriositeDirigeePlugin(BasePlugin):
    meta = Meta(
        name="curiosite_dirigee",
        priority=3.6,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        reponse = ctx.get("llm_response", "")
        suggestions = ctx.setdefault("questions_curiosite", [])

        if not reponse or not message:
            plugins_log.append("CuriositeDirigeePlugin : données insuffisantes.")
            return ctx

        # Très simple logique heuristique (peut être améliorée avec LLM local)
        if "je ne sais pas" in reponse.lower() or "peut-être" in reponse.lower() or "cela dépend" in reponse.lower():
            suggestions.append("Souhaites-tu me donner plus de détails pour que je m'améliore ?")
            suggestions.append("Y a-t-il une nuance que j’ai ratée ?")
            plugins_log.append("CuriositeDirigeePlugin : incertitude détectée → questions ajoutées")
            logger.info("[curiosite_dirigee] Question de clarification proposée.")

        return ctx
