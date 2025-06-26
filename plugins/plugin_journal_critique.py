"""
Plugin : journal_critique
Rôle : Archiver les commentaires de la critique intérieure dans un journal structuré
Priorité : 11
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.journal_critique")

class JournalCritiquePlugin(BasePlugin):
    meta = Meta(
        name="journal_critique",
        priority=11,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        critiques = ctx.get("critiques_internes", [])
        journal = ctx.setdefault("journal_critique", [])

        if not critiques:
            plugins_log.append("JournalCritiquePlugin : aucune critique à archiver")
            return ctx

        # Ne garde que la dernière critique
        dernière = critiques[-1]
        entrée = {
            "date": dernière.get("date", datetime.utcnow().isoformat()),
            "signature": dernière.get("signature", "👁 Anonyme"),
            "ton": dernière.get("ton", "neutre"),
            "commentaire": dernière.get("commentaire", ""),
            "cible": dernière.get("cible", "[aucune réponse]")
        }

        journal.append(entrée)
        ctx["journal_critique"] = journal
        plugins_log.append("JournalCritiquePlugin : critique archivée")
        logger.info(f"[journal_critique] Entrée ajoutée par {entrée['signature']}")

        return ctx
