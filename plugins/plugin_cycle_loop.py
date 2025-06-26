# plugins/core/plugin_cycle_loop.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.cycle_loop")


class PluginCycleLoop(BasePlugin):
    meta = Meta(
        name="plugin_cycle_loop",
        priority=-993,  # Après planificateur mais avant raisonnement
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        if not plan:
            logger.info("[cycle_loop] Aucun plan détecté.")
            return ctx

        # Trouver la prochaine étape à faire
        for step in plan:
            if step.get("status") == "à faire":
                ctx["tache_courante"] = step["étape"]
                step["status"] = "en cours"
                logger.info(f"[cycle_loop] Étape en cours : {step['étape']}")
                ctx.setdefault("plugins_log", []).append(f"CycleLoop : nouvelle étape en cours → {step['étape']}")
                break
        else:
            # Toutes les étapes sont terminées
            ctx["etat_cycle"] = "terminé"
            logger.info("[cycle_loop] Toutes les étapes ont été complétées.")
            ctx.setdefault("plugins_log", []).append("CycleLoop : plan complété.")
        
        return ctx
