"""
Plugin : synthese_dialectique
Rôle : Identifier les contradictions entre réponses et proposer une synthèse constructive
Priorité : 4 (après génération de réponses)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.synthese_dialectique")

class SyntheseDialectiquePlugin(BasePlugin):
    meta = Meta(
        name="synthese_dialectique",
        priority=4,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponses = ctx.get("llm_responses", [])

        # Filtrage
        valides = [r.strip() for r in reponses if r and r.strip()]
        if len(valides) < 2:
            plugins_log.append("SyntheseDialectiquePlugin : pas assez de matière pour synthèse")
            return ctx

        # Identification simplifiée des contradictions
        contradictions = []
        for i in range(len(valides)):
            for j in range(i+1, len(valides)):
                if valides[i].lower() != valides[j].lower() and valides[i][:20] != valides[j][:20]:
                    contradictions.append((valides[i], valides[j]))

        # Synthèse simple
        synthese = "Synthèse dialectique :\n"
        if contradictions:
            synthese += f"💥 {len(contradictions)} tensions détectées entre réponses.\n\n"
            for a, b in contradictions[:3]:
                synthese += f"- Contradiction entre :\nA: {a}\nB: {b}\n\n"
            synthese += "🤝 Tentative de conciliation : chaque point peut être vrai dans un contexte donné. Une fusion ou un choix conditionnel est suggéré."
        else:
            synthese += "✅ Aucune contradiction majeure détectée."

        ctx["synthese_dialectique"] = synthese
        plugins_log.append("SyntheseDialectiquePlugin : synthèse produite")
        logger.info("[synthese_dialectique] Synthèse générée")

        return ctx
