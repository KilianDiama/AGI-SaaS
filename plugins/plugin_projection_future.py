# plugins/plugin_projection_future.py

"""
Plugin : projection_future
Rôle   : Projette les étapes mentales futures pertinentes à partir de l’état cognitif actuel
Priorité : 98 (juste avant final_synthesis)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.projection_future")

class ProjectionFuturePlugin(BasePlugin):
    meta = Meta(
        name="projection_future",
        priority=98,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "")
        objections = ctx.get("contre_arguments", [])
        logique = ctx.get("emergence_logique", [])
        etat = ctx.get("etat_global", {})
        stabilite = etat.get("stabilite_cognitive", 100)

        projections = []

        # Projection 1 : continuer le raisonnement ?
        if objections:
            projections.append("Explorer ou répondre aux objections restantes.")

        # Projection 2 : compléter une structure logique ?
        if not logique:
            projections.append("Dégager les prémisses et implications non explicites.")

        # Projection 3 : vérifier la cohérence ?
        if stabilite < 60:
            projections.append("Stabiliser la charge cognitive ou simplifier le pipeline.")

        # Projection 4 : approfondir l’objectif ?
        if not objectif or len(objectif) < 10:
            projections.append("Clarifier ou reformuler l’objectif.")

        # Default
        if not projections:
            projections.append("Aucune action immédiate requise. Cycle complet.")

        ctx["prochaine_etapes_cognitives"] = projections
        log.append("ProjectionFuturePlugin : prochaines étapes projetées.")
        logger.info(f"[projection_future] Étapes anticipées : {projections}")

        return ctx
