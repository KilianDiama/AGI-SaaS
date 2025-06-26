"""
Plugin : apprentissage_par_cycle
Rôle : Enregistrer les actions et leurs retours pour favoriser un apprentissage autonome
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.apprentissage_par_cycle")

class ApprentissageParCyclePlugin(BasePlugin):
    meta = Meta(
        name="apprentissage_par_cycle",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire_exp = ctx.setdefault("memoire_experientielle", [])

        cycle_id = len(ctx.get("historique_evolution", []))
        timestamp = datetime.utcnow().isoformat()

        apprentissage = {
            "cycle": cycle_id,
            "timestamp": timestamp,
            "objectif": ctx.get("objectif", {}).get("but", "non défini"),
            "action": ctx.get("llm_response", "")[:200],
            "feedback": ctx.get("feedback_performance", "aucun"),
            "eval": ctx.get("evaluation_utilite", "non évalué")
        }

        memoire_exp.append(apprentissage)
        plugins_log.append("ApprentissageParCyclePlugin : expérience enregistrée")
        logger.info(f"[apprentissage_par_cycle] Cycle #{cycle_id} stocké")

        return ctx
