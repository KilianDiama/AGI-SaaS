"""
Plugin : reformulation_consensus
Rôle : Reformuler la réponse finale pour la rendre acceptable par tous les agents cognitifs impliqués
Priorité : 4.5 (après fusion ou réponse multi-rôle)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reformulation_consensus")

class ReformulationConsensusPlugin(BasePlugin):
    meta = Meta(
        name="reformulation_consensus",
        priority=4.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base = ctx.get("llm_response", "")

        if not base:
            return ctx

        prompt = (
            "Tu es un agent de consensus. Reformule la réponse suivante pour qu’elle soit :\n"
            "- Acceptable par des rôles cognitifs variés (logicien, créatif, prudent, etc.)\n"
            "- Neutre, claire, constructive\n"
            "- Optimisée pour une décision ou une application pratique\n\n"
            f"Réponse d’origine :\n{base.strip()}\n\n"
            "Ta reformulation :"
        )

        if ctx.get("invoke_llm"):
            reformule = await ctx["invoke_llm"](prompt)
            if reformule:
                ctx["llm_response"] = reformule.strip()
                ctx["response"] = ctx["llm_response"]
                plugins_log.append("ReformulationConsensusPlugin : reformulation finale de consensus")
                logger.info("[reformulation_consensus] Reformulation exécutée.")

        return ctx
