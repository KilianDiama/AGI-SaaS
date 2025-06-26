import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.plan_checker")

class PluginPlanChecker(BasePlugin):
    meta = Meta(
        name="plugin_plan_checker",
        version="1.0",
        priority=5.9,  # Juste avant export, après tout le reste
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        logs = ctx.setdefault("plugins_log", [])

        if not plan:
            logs.append("PluginPlanChecker : aucun plan trouvé ❌.")
            ctx["plan_status"] = "absent"
            return ctx

        terminées = [e for e in plan if e.get("status") == "fait"]
        restantes = [e for e in plan if e.get("status") != "fait"]

        if not restantes:
            ctx["plan_status"] = "complété"
            logs.append("PluginPlanChecker : toutes les étapes ont été accomplies ✅.")
        else:
            ctx["plan_status"] = "incomplet"
            ctx["plan_restantes"] = restantes
            logs.append(f"PluginPlanChecker : étapes restantes à accomplir : {[e['étape'] for e in restantes]} ⚠️.")

        logger.info(f"[plan_checker] Terminé = {len(terminées)} / {len(plan)}")
        return ctx
