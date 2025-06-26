"""
Plugin : cycle_autopoietique
Rôle : Automatiser un cycle d’auto-observation, d’analyse, et de proposition d’évolution
Priorité : 28
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.cycle_autopoietique")

class CycleAutopoietiquePlugin(BasePlugin):
    meta = Meta(
        name="cycle_autopoietique",
        priority=28,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        archive = ctx.get("feedback_archive", [])
        suggestions = ctx.setdefault("propositions_évolution", [])

        if not archive:
            ctx["cycle_autopoietique"] = "📭 Aucun cycle précédent. En attente d’observations futures."
            return ctx

        dernier = archive[-1]
        idée_plugin = {
            "nom": f"plugin_evolution_{len(suggestions)+1}",
            "objectif": "Mieux réagir aux contextes émotionnels complexes",
            "structure_suggérée": {
                "détecteur": "analyse le ton de la question",
                "réponse_adaptée": "modifie le style selon le contexte",
                "historique_affectif": "enregistre l’intensité émotionnelle"
            },
            "proposition_code": "# Plugin prototype à générer au prochain cycle"
        }

        suggestions.append({
            "date": datetime.utcnow().isoformat(),
            "résumé_du_cycle": {
                "input": dernier.get("input", ""),
                "réponse": dernier.get("réponse", ""),
                "critique": dernier.get("critique", ""),
            },
            "évolution_proposée": idée_plugin
        })

        ctx["propositions_évolution"] = suggestions
        ctx["cycle_autopoietique"] = (
            f"🔄 Cycle auto-évalué.\n"
            f"→ Prochaine extension suggérée : `{idée_plugin['nom']}`\n"
            f"Objectif : {idée_plugin['objectif']}\n"
            f"(stockée pour traitement futur)"
        )

        plugins_log.append("CycleAutopoietiquePlugin : nouvelle évolution proposée")
        logger.info("[cycle_autopoietique] Nouveau plugin proposé")

        return ctx
