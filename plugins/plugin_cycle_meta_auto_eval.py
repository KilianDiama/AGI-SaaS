# plugins/plugin_cycle_meta_auto_eval.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cycle_meta_auto_eval")

class PluginCycleMetaAutoEval(BasePlugin):
    meta = Meta(
        name="plugin_cycle_meta_auto_eval",
        priority=5.0,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_cycle_meta_auto_eval"

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "non défini")
        intention = ctx.get("intention", "indéfinie")
        note = ctx.get("evaluation_reponse", {}).get("note", -1)
        plugins = ctx.get("plugins_log", [])
        réponse = ctx.get("llm_response", "").strip()
        id_cycle = ctx.get("cycle_id", "inconnu")

        critique = {
            "cycle": id_cycle,
            "timestamp": datetime.utcnow().isoformat(),
            "note": note,
            "objectif": objectif,
            "intention": intention,
            "plugins_utilisés": [p.split(":")[0] for p in plugins if isinstance(p, str)],
            "réponse_vide": len(réponse) == 0,
            "qualité_estimée": (
                "faible" if note < 2 else
                "moyenne" if note < 4 else
                "bonne"
            )
        }

        logger.info(f"[{self.nom}] Bilan métacognitif du cycle {id_cycle} : {critique}")
        ctx.setdefault("meta_feedback_log", []).append(critique)
        ctx.setdefault("plugins_log", []).append(f"{self.nom} : bilan métacognitif généré")

        return ctx
