# plugins/plugin_logger_visuel.py

"""
Plugin : logger_visuel
Rôle   : Génère une trace JSON lisible des composants mentaux du cycle
Priorité : 103 (en toute fin de cycle)
Auteur  : Toi + GPT
"""

import json
from noyau_core import BasePlugin, Context, Meta

class LoggerVisuelPlugin(BasePlugin):
    meta = Meta(
        name="logger_visuel",
        priority=103,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        resume = {
            "objectif": ctx.get("objectif_general"),
            "noyau": ctx.get("noyau_conscient"),
            "symboles": ctx.get("symboles_expressifs", []),
            "concepts": [c["nom"] for c in ctx.get("concepts_crees", [])],
            "humeur": ctx.get("ton_emotionnel"),
            "ethique": ctx.get("diagnostic_ethique", {}),
            "narration": ctx.get("reflexion_narrative"),
            "auto_modifs": ctx.get("auto_modifications_proposees", []),
        }

        ctx["log_cognitif"] = json.dumps(resume, indent=2, ensure_ascii=False)
        return ctx
