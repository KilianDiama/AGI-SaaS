"""
Plugin : changelog_evolution
Rôle : Mémoriser l’historique des plugins générés, évalués et déployés par l’AGI
Priorité : 3.4 (dernier dans la chaîne d’auto-évolution)
Auteur : AGI & Matthieu
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.changelog_evolution")

class ChangelogEvolutionPlugin(BasePlugin):
    meta = Meta(
        name="changelog_evolution",
        priority=3.4,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        journal = ctx.setdefault("changelog_evolution", [])

        code_data = ctx.get("code_autogenere", {})
        eval_data = ctx.get("eval_plugin_propose", {})
        path = ctx.get("plugin_autodeploye", None)

        if not code_data:
            plugins_log.append("ChangelogEvolutionPlugin : aucun code à archiver.")
            return ctx

        ligne = {
            "timestamp": datetime.utcnow().isoformat(),
            "proposition": code_data.get("proposition"),
            "note": eval_data.get("note", 0),
            "path": path,
            "etat": "déployé" if path else "rejeté"
        }

        journal.append(ligne)
        plugins_log.append(f"ChangelogEvolutionPlugin : entrée ajoutée → {ligne['etat']} [{ligne['proposition']}]")
        logger.info("[changelog_evolution] Historique mis à jour.")

        return ctx
