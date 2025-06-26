"""
Plugin : trace_cognitive
Rôle : Suivre et journaliser les décisions internes, mutations, ajustements et conflits cognitifs
Priorité : 0.9 (tout début du cycle, avant tout le reste)
Auteur : AGI & Matthieu
"""

import logging
import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.trace_cognitive")

class TraceCognitivePlugin(BasePlugin):
    meta = Meta(
        name="trace_cognitive",
        priority=0.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        trace = ctx.setdefault("trace_cognitive", [])
        plugins_log = ctx.setdefault("plugins_log", [])
        horodatage = datetime.datetime.utcnow().isoformat()

        evenement = {
            "time": horodatage,
            "message": ctx.get("message", "")[:150],
            "etat": {
                "objectif": ctx.get("objectif_externe", "non défini"),
                "memoire": ctx.get("memoire_reinjectee", []),
                "concepts": ctx.get("concepts_memorises", []),
                "decision": ctx.get("decision_simulee", "n/a")
            }
        }

        trace.append(evenement)
        plugins_log.append("TraceCognitivePlugin : trace ajoutée")
        logger.info(f"[trace_cognitive] Événement journalisé à {horodatage}")

        return ctx
