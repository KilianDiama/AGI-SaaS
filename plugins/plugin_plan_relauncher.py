import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.plan_relauncher")

class PluginPlanRelauncher(BasePlugin):
    meta = Meta(
        name="plugin_plan_relauncher",
        version="1.0",
        priority=6.0,  # Après plan_checker, juste avant fermeture
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.setdefault("plugins_log", [])
        plan_status = ctx.get("plan_status", "")
        restantes = ctx.get("plan_restantes", [])

        if plan_status != "incomplet" or not restantes:
            logs.append("PluginPlanRelauncher : rien à relancer.")
            return ctx

        # Redéclenche un objectif ciblé
        ctx["objectif"] = {
            "but": "terminer le plan existant",
            "état": "relancé",
            "priorité": 1,
        }
        ctx["tache_courante"] = restantes[0]["étape"]
        logs.append(f"PluginPlanRelauncher : plan relancé à l’étape → {restantes[0]['étape']} 🔁")

        logger.info(f"[plan_relauncher] Redémarrage à : {restantes[0]['étape']}")
        return ctx
