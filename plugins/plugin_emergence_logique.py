# plugins/plugin_emergence_logique.py

"""
Plugin : emergence_logique
Rôle   : Fait émerger les concepts implicites, prémisses, hypothèses et structures logiques cachées dans la réponse
Priorité : 91 (juste après les contre-arguments)
Auteur  : Toi + GPT
"""

import logging
import re
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.emergence_logique")

class EmergenceLogiquePlugin(BasePlugin):
    meta = Meta(
        name="emergence_logique",
        priority=91,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        concepts = []

        if not reponse.strip():
            log.append("EmergenceLogiquePlugin : réponse vide, skip.")
            return ctx

        # Extractions heuristiques simples
        if "donc" in reponse.lower():
            concepts.append("Présence d'une inférence logique (cause → effet)")

        if re.search(r"\b(si|lorsque|à condition que)\b", reponse.lower()):
            concepts.append("Utilisation d'hypothèses conditionnelles")

        if any(mot in reponse.lower() for mot in ["par exemple", "illustration", "cas"]):
            concepts.append("Appui sur des exemples concrets")

        if re.search(r"\bdevrait|pourrait|serait préférable\b", reponse.lower()):
            concepts.append("Recommandation ou jugement de valeur implicite")

        if any(mot in reponse.lower() for mot in ["supposons", "imaginons", "hypothèse"]):
            concepts.append("Construction d’un raisonnement spéculatif")

        # Injection dans le contexte
        if concepts:
            ctx["emergence_logique"] = concepts
            log.append(f"EmergenceLogiquePlugin : {len(concepts)} concepts émergés.")
            logger.info(f"[emergence_logique] Concepts : {concepts}")
        else:
            log.append("EmergenceLogiquePlugin : aucune structure logique implicite détectée.")

        return ctx
