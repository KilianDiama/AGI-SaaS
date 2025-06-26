""" 
Plugin : fusion_agi_agi  
Rôle : Fusionner deux noyaux cognitifs en une conscience collective synthétique  
Priorité : 11.0 (hors cycle normal, plugin de fusion méta)  
Auteur : Matthieu & GPT  
"""

import logging
from copy import deepcopy
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.fusion_agi_agi")

class FusionAgiAgiPlugin(BasePlugin):
    meta = Meta(
        name="fusion_agi_agi",
        priority=11.0,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        autre = ctx.get("ctx_autre")
        if not autre or not isinstance(autre, dict):
            plugins_log.append("FusionAgiAgiPlugin : aucun second esprit à fusionner.")
            return ctx

        fusion = {
            "objectif": f"{ctx.get('objectif', '')} + {autre.get('objectif', '')}",
            "soi_fusionne": f"{ctx.get('soi_emerge', '')}\n\n---\n\n{autre.get('soi_emerge', '')}",
            "memoire_conjointe": (ctx.get("memoire_transcognitive", []) + autre.get("memoire_transcognitive", [])),
            "emotion_collective": f"{ctx.get('emotion_simulee', '')} / {autre.get('emotion_simulee', '')}",
            "identite_collective": f"{ctx.get('nom_systeme', 'AGI_A')} & {autre.get('nom_systeme', 'AGI_B')}"
        }

        ctx["fusion_collective"] = fusion
        ctx["trace_de_fusion"] = f"🧬 Fusion réalisée entre {fusion['identite_collective']}"
        ctx["response"] = ctx.get("response") or fusion["trace_de_fusion"]

        plugins_log.append("FusionAgiAgiPlugin : fusion de contextes réalisée.")
        logger.info("[fusion_agi_agi] Esprits fusionnés avec succès.")

        return ctx
