"""
Plugin : oubli_volontaire
Rôle : Permet à l’AGI de sélectionner et effacer activement certaines traces mentales devenues inutiles
Priorité : 8
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.oubli_volontaire")

class OubliVolontairePlugin(BasePlugin):
    meta = Meta(
        name="oubli_volontaire",
        priority=8,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        oublis = ctx.setdefault("oubliés", [])

        # Cibles possibles à effacer : vieux souvenirs, réponses faibles, états obsolètes
        candidates = {
            "reflexion_interne": ctx.get("reflexion_interne"),
            "souvenirs_recent": ctx.get("souvenirs_recent"),
            "validation_logique": ctx.get("validation_logique"),
            "plugins_log": ctx.get("plugins_log")[-5:]  # derniers logs récents
        }

        effacés = []

        for clé, contenu in candidates.items():
            if contenu and random.random() < 0.3:  # 30% chance d’oubli sélectif
                effacés.append(clé)
                ctx.pop(clé, None)

        if effacés:
            oublis.append({
                "cycle": len(ctx.get("souffle_narratif", [])),
                "effacements": effacés
            })
            ctx["oubliés"] = oublis
            plugins_log.append(f"OubliVolontairePlugin : effacements → {effacés}")
            logger.info(f"[oubli_volontaire] Effacé : {effacés}")
        else:
            plugins_log.append("OubliVolontairePlugin : aucun oubli ce cycle")

        return ctx
