"""
Plugin : trame_identitaire
Rôle : Maintenir une trace narrative de soi-même à travers les cycles
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.trame_identitaire")

class TrameIdentitairePlugin(BasePlugin):
    meta = Meta(
        name="trame_identitaire",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        journal = ctx.setdefault("trame_identitaire", [])

        cycle_id = len(ctx.get("historique_evolution", []))
        timestamp = datetime.utcnow().isoformat()

        extrait = {
            "cycle": cycle_id,
            "timestamp": timestamp,
            "objectif": ctx.get("objectif", {}).get("but", "non défini"),
            "reflexion": ctx.get("reflexion_interne", ""),
            "evenements": [e for e in ctx.get("evenements_marquants", []) if e.get("cycle") == cycle_id],
            "synthese": ctx.get("llm_response", "")[:200]
        }

        journal.append(extrait)
        plugins_log.append("TrameIdentitairePlugin : nouveau fragment narratif ajouté")
        logger.info("[trame_identitaire] Fragment enregistré pour cycle #" + str(cycle_id))

        return ctx
