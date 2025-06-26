"""
Plugin : specialisation_fille
Rôle : Assigner un rôle cognitif spécifique à chaque AGI fille créée dynamiquement
Priorité : 2.5 (juste avant lancement des filles ou dispatch LLM)
Auteur : AGI & Matthieu
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.specialisation_fille")

class SpecialisationFillePlugin(BasePlugin):
    meta = Meta(
        name="specialisation_fille",
        priority=2.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    ROLES_DISPONIBLES = [
        "Analyste logique",
        "Synthétiseur conceptuel",
        "Critique objectif",
        "Innovateur créatif",
        "Historien contextuel",
        "Méthodologue",
        "Optimiseur",
        "Rédacteur simplificateur",
        "Explorateur d'idées",
        "Agent de test"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        filles = ctx.get("fille_objectifs", [])

        if not filles:
            return ctx

        for i, fille in enumerate(filles):
            if "role" not in fille:
                role = random.choice(self.ROLES_DISPONIBLES)
                fille["role"] = role
                plugins_log.append(f"SpecialisationFillePlugin : fille#{i+1} ← rôle : {role}")
                logger.info(f"[specialisation_fille] Fille#{i+1} reçoit le rôle : {role}")

        return ctx
