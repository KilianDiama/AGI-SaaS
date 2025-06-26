# plugins/plugin_heuristique_adaptative.py

import logging
from collections import defaultdict
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.heuristique_adaptative")

class PluginHeuristiqueAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_heuristique_adaptative",
        priority=3.6,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.memoire_plugins = defaultdict(list)
        self.nom = "plugin_heuristique_adaptative"

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "aucun")
        tonalite = ctx.get("tonalite_utilisateur", "neutre")
        note = ctx.get("evaluation_reponse", {}).get("note", 0)
        plugins_utilises = ctx.get("plugins_log", [])
        cycle_id = ctx.get("cycle_id")

        # 🧠 Mémorisation des plugins utilisés avec leur efficacité
        for log_entry in plugins_utilises:
            plugin_name = log_entry.split(":")[0].strip()
            self.memoire_plugins[(objectif, tonalite)].append({
                "plugin": plugin_name,
                "note": note,
                "timestamp": datetime.utcnow().isoformat(),
                "cycle": cycle_id
            })

        # 📊 Calcul heuristique
        scores = defaultdict(float)
        for trace in self.memoire_plugins.get((objectif, tonalite), []):
            scores[trace["plugin"]] += float(trace["note"] or 0)

        plugins_optimaux = sorted(scores.items(), key=lambda x: -x[1])
        top_plugins = [plugin for plugin, score in plugins_optimaux[:3]]

        # 💡 Suggestion proactive
        if top_plugins:
            ctx["plugins_suggérés"] = top_plugins
            logger.info(f"[{self.nom}] Plugins suggérés pour '{objectif}' ({tonalite}) → {top_plugins}")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : recommandation = {top_plugins}")

        return ctx
