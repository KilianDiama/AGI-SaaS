from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.executant_plan")

class PluginExecutantPlan(BasePlugin):
    meta = Meta(
        name="plugin_executant_plan",
        version="1.0",
        priority=3.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        if not plan:
            logger.info("[executant_plan] Aucun plan détecté.")
            ctx.setdefault("plugins_log", []).append("PluginExecutantPlan : aucun plan.")
            return ctx

        for step in plan:
            if step["status"] == "à faire":
                step["status"] = "en cours"
                ctx["tache_courante"] = step["étape"]
                logger.info(f"[executant_plan] Étape activée → {step['étape']}")
                ctx.setdefault("plugins_log", []).append(
                    f"PluginExecutantPlan : étape en cours → {step['étape']}"
                )
                return ctx

        logger.info("[executant_plan] Toutes les étapes sont complètes.")
        ctx["tache_courante"] = None
        ctx.setdefault("plugins_log", []).append("PluginExecutantPlan : plan terminé.")
        return ctx
