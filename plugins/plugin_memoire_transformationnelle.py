"""
Plugin : memoire_transformationnelle
Rôle : Enregistrer les transformations, leurs déclencheurs, et leur impact
Priorité : 30
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.memoire_transformationnelle")

class MemoireTransformationnellePlugin(BasePlugin):
    meta = Meta(
        name="memoire_transformationnelle",
        priority=30,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        mémoire = ctx.setdefault("journal_transformation", [])

        dernier_plugin = ctx.get("plugin_recent", "inconnu")
        situation = ctx.get("message", "aucun contexte")
        état = ctx.get("état_interieur", {})
        timestamp = datetime.utcnow().isoformat()

        mémoire.append({
            "timestamp": timestamp,
            "déclencheur": situation,
            "plugin": dernier_plugin,
            "impact_ressenti": état.get("ton", "non spécifié"),
            "structure_intérieure": état
        })

        ctx["journal_transformation"] = mémoire
        log.append(f"MemoireTransformationnellePlugin : transformation archivée ({dernier_plugin})")
        logger.info(f"[memoire_transformationnelle] Changement noté : {dernier_plugin}")

        return ctx
