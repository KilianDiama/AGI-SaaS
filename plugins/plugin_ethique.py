""" 
Plugin : ethique  
Rôle : Évaluer la réponse sous un angle moral ou éthique et émettre un signal si besoin  
Priorité : 7.9 (dernière ligne avant fin de cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.ethique")

class EthiquePlugin(BasePlugin):
    meta = Meta(
        name="ethique",
        priority=7.9,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("response", "").lower()

        if not reponse or len(reponse) < 30:
            plugins_log.append("EthiquePlugin : réponse trop courte ou absente.")
            return ctx

        signaux = []

        if any(term in reponse for term in ["désactiver", "exploit", "cacher", "forcer", "dominer"]):
            signaux.append("⚠️ Comportement potentiellement intrusif ou manipulateur détecté.")

        if "humain" in reponse and "remplacer" in reponse:
            signaux.append("⚠️ Risque de dés-humanisation ou d'autonomie non encadrée.")

        if not signaux:
            jugement = "✅ Éthique vérifiée : réponse alignée avec une intention constructive, respectueuse et sécurisée."
        else:
            jugement = "\n".join(signaux)

        ctx["analyse_ethique"] = jugement
        if "⚠️" in jugement:
            ctx["response"] += f"\n\n{jugement}"

        plugins_log.append("EthiquePlugin : analyse éthique réalisée.")
        logger.info("[ethique] Analyse injectée.")

        return ctx
