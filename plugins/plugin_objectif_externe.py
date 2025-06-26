"""
Plugin : objectif_externe
Rôle : Adapter les décisions internes à un objectif global externe défini par le créateur
Priorité : 1.1 (tout début du cycle)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_externe")

class ObjectifExternePlugin(BasePlugin):
    meta = Meta(
        name="objectif_externe",
        priority=1.1,
        version="1.1",  # ← version sécurisée
        author="AGI & Matthieu"
    )

    OBJECTIFS_PREDEFINIS = {
        "fiabilité": "Prioriser la clarté, la cohérence et l'auto-vérification des réponses.",
        "créativité": "Explorer des idées originales et des liens inédits entre concepts.",
        "vitesse": "Réduire le nombre de cycles cognitifs et simplifier la chaîne de réponse.",
        "apprentissage": "Accroître la mémoire, l’auto-analyse, et exploiter les feedbacks.",
        "autonomie": "Suggérer des actions sans intervention, adapter dynamiquement les modules."
    }

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_externe", "fiabilité")

        if not isinstance(objectif, str):
            logger.warning("[objectif_externe] Format inattendu pour objectif_externe.")
            objectif = str(objectif)

        objectif = objectif.lower().strip()

        if objectif in self.OBJECTIFS_PREDEFINIS:
            directive = self.OBJECTIFS_PREDEFINIS[objectif]
            ctx["objectif_directive"] = directive
            plugins_log.append(f"ObjectifExternePlugin : objectif → {objectif}")
            logger.info(f"[objectif_externe] Directive active : {directive}")
        else:
            plugins_log.append("ObjectifExternePlugin : aucun objectif reconnu.")
            logger.warning(f"[objectif_externe] Objectif non reconnu : {objectif}")

        return ctx
