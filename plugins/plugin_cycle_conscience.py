"""
Plugin : cycle_conscience
Rôle : Exécuter un cycle réflexif complet : critique → apaisement → archive
Priorité : 13 (à la fin du run)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.cycle_conscience")

class CycleConsciencePlugin(BasePlugin):
    meta = Meta(
        name="cycle_conscience",
        priority=13,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        réponse = ctx.get("llm_response", "").strip()
        critiques = ctx.get("critiques_internes", [])
        veilleuses = ctx.get("voix_veilleuse", [])
        journal_global = ctx.setdefault("archives_conscience", [])

        if not réponse:
            plugins_log.append("CycleConsciencePlugin : aucune réponse pour introspection")
            return ctx

        entrée = {
            "date": datetime.utcnow().isoformat(),
            "réponse": réponse,
            "critique": critiques[-1] if critiques else None,
            "apaisement": veilleuses[-1] if veilleuses else None
        }

        journal_global.append(entrée)
        ctx["archives_conscience"] = journal_global

        plugins_log.append("CycleConsciencePlugin : cycle d'introspection archivé")
        logger.info("[cycle_conscience] Cycle complet sauvegardé")

        return ctx
