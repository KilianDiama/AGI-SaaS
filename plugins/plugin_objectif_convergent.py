"""
Plugin : objectif_convergent
Rôle : Injecter un objectif global dans toutes les AGI filles ou modules dérivés
Priorité : 1.2 (juste après l’objectif externe principal)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_convergent")

class ObjectifConvergentPlugin(BasePlugin):
    meta = Meta(
        name="objectif_convergent",
        priority=1.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_externe", None)

        if not objectif:
            return ctx

        sous_taches = ctx.get("sous_taches", [])
        filles = ctx.setdefault("fille_objectifs", [])

        # Injecte l'objectif dans chaque tâche fille à venir
        for i, tache in enumerate(sous_taches):
            filles.append({
                "tache": tache,
                "objectif": objectif
            })

        if filles:
            logger.info(f"[objectif_convergent] Objectif partagé injecté à {len(filles)} sous-tâches.")
            plugins_log.append("ObjectifConvergentPlugin : objectif partagé vers filles")

        return ctx
