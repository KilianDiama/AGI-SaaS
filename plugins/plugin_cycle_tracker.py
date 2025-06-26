"""
Plugin : cycle_tracker
Rôle : Suivre et enregistrer l'évolution des cycles cognitifs au fil du temps
Priorité : 1 (très tôt dans le cycle)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.cycle_tracker")

class CycleTrackerPlugin(BasePlugin):
    meta = Meta(
        name="cycle_tracker",
        priority=1,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        cycle_data = ctx.setdefault("cycle_data", {})

        # Initialiser le profil de cycle courant
        now = datetime.utcnow().isoformat()
        cycle = {
            "timestamp": now,
            "objectif": ctx.get("objectif", {}).get("but", "inconnu"),
            "memoire_active": ctx.get("memoire", {}).get("active", []),
            "etat_conscient": ctx.get("soi", "non défini"),
            "taille_contexte": len(str(ctx)),
        }

        # Stocker dans la mémoire longue (si elle existe)
        historique = ctx.setdefault("meta_cycle_history", [])
        historique.append(cycle)

        # Limiter la taille de l’historique pour éviter surcharge
        if len(historique) > 100:
            historique.pop(0)

        plugins_log.append("CycleTrackerPlugin : cycle enregistré")
        logger.info(f"[cycle_tracker] Cycle enregistré à {now}")

        return ctx
