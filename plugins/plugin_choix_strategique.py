# plugins/plugin_choix_strategique.py
from noyau_core import BasePlugin, Context, Meta
import logging
import hashlib
import json

logger = logging.getLogger("plugin.choix_strategique")

class PluginChoixStrategique(BasePlugin):
    meta = Meta(
        name="plugin_choix_strategique",
        version="1.0",
        priority=97.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "")
        tonalite = ctx.get("tonalite_utilisateur", "")
        utilisateur = ctx.get("user", {}).get("email", "anonyme")
        memoire = ctx.get("memoire_strategique", {})

        if not objectif or not memoire:
            ctx.setdefault("plugins_log", []).append("PluginChoixStrategique : aucun objectif ou mémoire.")
            return ctx

        best_score = -float("inf")
        best_plan = None

        for trace in memoire.values():
            if trace["objectif"] == objectif and trace["utilisateur"] == utilisateur:
                score = trace["note"] + trace.get("alignement", 0)
                if score > best_score:
                    best_score = score
                    best_plan = trace.get("plan")

        if best_plan:
            ctx["plan"] = best_plan
            ctx.setdefault("plugins_log", []).append(f"PluginChoixStrategique : plan restauré (score={best_score}).")
        else:
            ctx.setdefault("plugins_log", []).append("PluginChoixStrategique : aucun plan restauré.")

        return ctx
