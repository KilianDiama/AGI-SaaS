"""
Plugin : rituel_cycle
Rôle : Créer un rituel d’ouverture et de clôture pour chaque cycle cognitif
Priorité : 0 et 7 (doit être appelé en ouverture et clôture)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.rituel_cycle")

class RituelCyclePlugin(BasePlugin):
    meta = Meta(
        name="rituel_cycle",
        priority=0,  # Début de cycle (à réutiliser avec priority=7 si exécuté deux fois)
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        historique = ctx.setdefault("rituels", {})

        cycle_id = len(ctx.get("historique_evolution", []))
        moment = ctx.get("moment_cycle", "début")  # doit être défini en amont

        if moment == "début":
            intention = f"🌄 Cycle {cycle_id} : Ouverture avec intention d'explorer le but '{ctx.get('objectif', {}).get('but', 'non défini')}'."
            historique[cycle_id] = {"intention": intention}
            ctx["rituel_ouverture"] = intention
            plugins_log.append("RituelCyclePlugin : ouverture posée")
            logger.info(f"[rituel_cycle] {intention}")

        elif moment == "fin":
            integration = f"🌙 Cycle {cycle_id} : Clôture. Réponse principale : '{ctx.get('llm_response', '')[:120]}...'"
            historique[cycle_id]["integration"] = integration
            ctx["rituel_cloture"] = integration
            plugins_log.append("RituelCyclePlugin : clôture générée")
            logger.info(f"[rituel_cycle] {integration}")

        return ctx
