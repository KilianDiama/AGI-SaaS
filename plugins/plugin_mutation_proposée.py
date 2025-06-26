"""
Plugin : mutation_proposée
Rôle : Détecter une faiblesse ou boucle inefficace et proposer une mutation ou remplacement de module
Priorité : 3.4 (juste après analyse ou raisonnement)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.mutation_proposee")

class MutationProposeePlugin(BasePlugin):
    meta = Meta(
        name="mutation_proposee",
        priority=3.4,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTIFS_MUTATION = [
        ("trop lent", "optimiser les plugins critiques ou simplifier le raisonnement"),
        ("contradiction", "ajuster la mémoire ou le raisonnement logique"),
        ("pas compris", "améliorer l'analyse contextuelle ou tonalité utilisateur"),
        ("je ne sais pas", "renforcer l’accès à un LLM plus large ou à un plugin conceptuel")
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()
        feedback = ctx.get("feedback_utilisateur", "").lower()
        suggestions = ctx.setdefault("mutations_proposees", [])

        for motif, suggestion in self.MOTIFS_MUTATION:
            if motif in message or motif in feedback:
                suggestion_msg = f"⚠️ Détection : '{motif}' → Proposition : {suggestion}"
                suggestions.append(suggestion_msg)
                plugins_log.append(f"MutationProposeePlugin : mutation suggérée → {motif}")
                logger.warning(f"[mutation_proposee] Suggestion de mutation : {suggestion_msg}")
                break

        return ctx
