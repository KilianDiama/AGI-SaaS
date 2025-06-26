# plugins/plugin_genese_nouvel_objectif.py

"""
Plugin : genese_nouvel_objectif
Rôle   : Génère un objectif autonome si aucun n’est fourni, basé sur mémoire, état et contexte
Priorité : -5 (tout début de cycle)
Auteur  : Toi + GPT
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.genese_nouvel_objectif")

class GeneseNouvelObjectifPlugin(BasePlugin):
    meta = Meta(
        name="genese_nouvel_objectif",
        priority=-5,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "").strip()

        if objectif:
            log.append("GeneseNouvelObjectifPlugin : objectif déjà présent — skip.")
            return ctx

        themes = [b["theme"] for b in ctx.get("memoires_emergentes", [])]
        suggestions = [
            "Explorer une contradiction non résolue",
            "Améliorer une réponse passée imparfaite",
            "Synthétiser un concept émergent",
            "Clarifier les intentions de l'utilisateur",
            "Stabiliser l'état cognitif interne",
        ]

        if themes:
            choix = random.choice(themes)
            new_objectif = f"Approfondir le thème {choix}"
        else:
            new_objectif = random.choice(suggestions)

        ctx["objectif_general"] = new_objectif
        log.append(f"GeneseNouvelObjectifPlugin : nouvel objectif autonome = « {new_objectif} »")
        logger.info(f"[genese_nouvel_objectif] Objectif généré : {new_objectif}")

        return ctx
