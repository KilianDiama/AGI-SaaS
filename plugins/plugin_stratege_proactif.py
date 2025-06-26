# plugins/plugin_stratege_proactif.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.stratege_proactif")

class PluginStrategeProactif(BasePlugin):
    meta = Meta(
        name="plugin_stratege_proactif",
        version="1.0",
        author="Toi & GPT",
        priority=3.8
    )

    def __init__(self):
        self.nom = "plugin_stratege_proactif"

    async def run(self, ctx: Context) -> Context:
        intentions = ctx.get("historique_intentions", [])
        mem_strategie = ctx.setdefault("plan_long_terme", {})
        now = datetime.utcnow().isoformat()

        if not intentions:
            logger.info(f"[{self.nom}] Aucune intention historique détectée.")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : pas d'intention à analyser.")
            return ctx

        tendances = self._extraire_tendances(intentions)
        plan = self._generer_plan(tendances)

        mem_strategie["dernière_mise_à_jour"] = now
        mem_strategie["tendances"] = tendances
        mem_strategie["plan"] = plan

        ctx.setdefault("plugins_log", []).append(f"{self.nom} : planification long terme injectée.")
        return ctx

    def _extraire_tendances(self, intentions: list) -> dict:
        stats = {}
        for intent in intentions:
            stats[intent] = stats.get(intent, 0) + 1
        return dict(sorted(stats.items(), key=lambda x: -x[1]))

    def _generer_plan(self, tendances: dict) -> list:
        return [
            {
                "objectif": f"Approfondir la capacité à « {intention} »",
                "priorité": count,
                "status": "à faire"
            }
            for intention, count in tendances.items()
        ]
