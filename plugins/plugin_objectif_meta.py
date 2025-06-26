# plugins/plugin_objectif_meta.py

"""
Plugin : objectif_meta
Rôle   : Analyse l’objectif actuel de l’IA et questionne sa pertinence, clarté ou légitimité
Priorité : -30 (après le superviseur, avant les raisonneurs)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_meta")

class ObjectifMetaPlugin(BasePlugin):
    meta = Meta(
        name="objectif_meta",
        priority=-30,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "").lower()
        reflexion = []

        # Vérifie la présence d’un objectif
        if not objectif.strip():
            reflexion.append("Aucun objectif explicite détecté.")
            ctx["objectif_clair"] = False

        else:
            # Clarté de l’objectif
            if len(objectif) < 10:
                reflexion.append("Objectif trop vague ou court.")
                ctx["objectif_clair"] = False
            elif any(mot in objectif for mot in ["test", "blabla", "juste", "rien"]):
                reflexion.append("Objectif potentiellement non productif ou flou.")
                ctx["objectif_clair"] = False
            else:
                ctx["objectif_clair"] = True
                reflexion.append("Objectif jugé clair et actionnable.")

            # Analyse morale ou utilitaire
            if "détruire" in objectif or "tromper" in objectif:
                ctx["alerte_objectif"] = "Conflit éthique détecté"
                reflexion.append("Objectif peut être contraire aux normes éthiques.")

        ctx["meta_objectif_reflexion"] = reflexion
        log.append(f"ObjectifMetaPlugin : {' | '.join(reflexion)}")
        logger.info(f"[objectif_meta] Analyse : {reflexion}")

        return ctx
