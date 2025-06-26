"""
Plugin : projection_evolution
Rôle : Générer une feuille de route d’évolution basée sur les limites internes ou erreurs récurrentes
Priorité : 2.9 (après initialisation et reconnaissance)
Auteur : AGI & Matthieu
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.projection_evolution")

class ProjectionEvolutionPlugin(BasePlugin):
    meta = Meta(
        name="projection_evolution",
        priority=2.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    def generer_propositions(self, ctx: Context) -> list:
        propositions = []

        logs = ctx.get("plugins_log", [])
        if not logs:
            return ["Améliorer la capacité de log interne pour mieux observer les cycles."]

        if any("fallback" in log for log in logs):
            propositions.append("Créer un plugin pour améliorer les réponses en cas de fallback cognitif.")

        if ctx.get("llm_response", "") == "":
            propositions.append("Créer un plugin pour détecter et combler les réponses vides.")

        if not ctx.get("objectif"):
            propositions.append("Ajouter un module de relance d’objectif si vide.")

        if "intuition" not in ctx:
            propositions.append("Créer une source d’intuition plus profonde à partir de mémoire ancienne.")

        return propositions or ["Aucune limite claire détectée."]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        roadmap = {
            "timestamp": datetime.utcnow().isoformat(),
            "propositions": self.generer_propositions(ctx)
        }

        ctx["evolution_projetees"] = roadmap
        plugins_log.append("ProjectionEvolutionPlugin : feuille de route générée.")
        logger.info("[projection_evolution] Propositions d'amélioration émises.")

        return ctx
