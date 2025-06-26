"""
Plugin : trace_evolution
Rôle : Suivre l'évolution cognitive au fil du temps (cycles, modules, complexité)
Priorité : 5 (fin de cycle)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.trace_evolution")

class TraceEvolutionPlugin(BasePlugin):
    meta = Meta(
        name="trace_evolution",
        priority=5,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        historique = ctx.setdefault("historique_evolution", [])

        cycle_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "objectif": ctx.get("objectif", {}).get("but", "non défini"),
            "capacites": list(ctx.get("capacites_cartographie", {}).get("actives", [])),
            "memoire_long_terme_size": len(ctx.get("memoire", {}).get("long_terme", [])),
            "taille_contexte": len(str(ctx))
        }

        historique.append(cycle_info)

        # Pour éviter surcharge mémoire
        if len(historique) > 200:
            historique.pop(0)

        resume = f"📊 Cycle #{len(historique)} enregistré. Capacités actives : {len(cycle_info['capacites'])}, souvenirs : {cycle_info['memoire_long_terme_size']}."

        ctx["trace_evolution"] = resume
        plugins_log.append("TraceEvolutionPlugin : cycle tracé")
        logger.info("[trace_evolution] " + resume)

        return ctx
