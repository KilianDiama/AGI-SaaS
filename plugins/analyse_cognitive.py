"""
Plugin : analyse_cognitive
Rôle : Identifier les éléments clés cognitifs présents dans la réponse générée
Priorité : 4.5 (entre raisonnement et synthèse)
Auteur : Matthieu & GPT
"""

import logging
import re
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.analyse_cognitive")

class AnalyseCognitivePlugin(BasePlugin):
    meta = Meta(
        name="analyse_cognitive",
        priority=4.5,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("response", "")

        if not isinstance(reponse, str) or not reponse.strip():
            plugins_log.append("AnalyseCognitivePlugin : réponse vide ou invalide.")
            return ctx

        # Recherche de patrons cognitifs simples
        motifs = {
            "introspection": r"\b(je pense|je crois|il me semble|je ressens)\b",
            "justification": r"\b(parce que|car|donc|ce qui implique)\b",
            "projection": r"\b(demain|dans le futur|pourrait être|sera)\b",
            "évaluation": r"\b(meilleur|pire|efficace|pertinent)\b"
        }

        resultats = {}
        for cle, regex in motifs.items():
            matchs = re.findall(regex, reponse, re.IGNORECASE)
            if matchs:
                resultats[cle] = len(matchs)

        ctx["analyse_cognitive"] = resultats or {"note": "Aucun schéma cognitif évident."}
        plugins_log.append(f"AnalyseCognitivePlugin : {len(resultats)} motifs cognitifs détectés.")
        logger.info("[analyse_cognitive] Analyse : " + str(resultats))

        return ctx
