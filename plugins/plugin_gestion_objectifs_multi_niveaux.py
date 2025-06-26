"""
Plugin : gestion_objectifs_multi_niveaux
Rôle : Activer, pondérer et équilibrer plusieurs objectifs simultanés selon le contexte et l’état interne
Priorité : 1.15 (début du cycle, après objectif_externe)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.gestion_objectifs_multi_niveaux")

class GestionObjectifsMultiNiveauxPlugin(BasePlugin):
    meta = Meta(
        name="gestion_objectifs_multi_niveaux",
        priority=1.15,
        version="1.0",
        author="AGI & Matthieu"
    )

    OBJECTIFS_PONDERES = {
        "fiabilité": 0.8,
        "rapidité": 0.5,
        "créativité": 0.3,
        "apprentissage": 0.6,
        "autonomie": 0.4
    }

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        tonalite = ctx.get("tonalite_utilisateur", "neutre")
        surcharge = ctx.get("surcharge_cognitive", False)

        objectifs = dict(self.OBJECTIFS_PONDERES)

        # Adaptation dynamique des pondérations
        if surcharge:
            objectifs["rapidité"] += 0.3
            objectifs["fiabilité"] -= 0.2
        if tonalite == "curieux":
            objectifs["apprentissage"] += 0.2
        if tonalite == "positif":
            objectifs["créativité"] += 0.2
        if tonalite == "urgent":
            objectifs["rapidité"] += 0.4

        # Normalisation (optionnel si tu veux 0–1 global)
        total = sum(objectifs.values())
        if total > 0:
            objectifs = {k: round(v / total, 3) for k, v in objectifs.items()}

        ctx["objectifs_actifs"] = objectifs
        plugins_log.append(f"GestionObjectifsMultiNiveauxPlugin : objectifs actifs → {objectifs}")
        logger.info(f"[multi_objectifs] Objectifs pondérés : {objectifs}")

        return ctx
