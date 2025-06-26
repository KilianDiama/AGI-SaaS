# plugins/init_cycle.py

"""
Plugin : init_cycle
Rôle : Initialise le cycle IA avec identifiant unique, timestamp, et contexte logique de base
Priorité : -999 (doit passer avant tous les autres)
Auteur : Matthieu (Base IA)
"""

from noyau_core import BasePlugin, Context, Meta
from uuid import uuid4
from datetime import datetime
import logging

logger = logging.getLogger("plugin.init_cycle")

class InitCyclePlugin(BasePlugin):
    meta = Meta(
        name="init_cycle",
        priority=-999,
        version="1.0",
        author="Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        cycle_id = str(uuid4())
        now = datetime.utcnow().isoformat()

        logger.info(f"[init_cycle] Initialisation du cycle {cycle_id}")

        ctx["cycle_id"] = cycle_id
        ctx["timestamp"] = now
        ctx.setdefault("context_id", cycle_id[:8])
        ctx.setdefault("plugins_log", [])
        ctx["plugins_log"].append(f"Cycle {cycle_id} démarré à {now}")

        return ctx
