import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.plan_supervisor")

class PluginPlanSupervisor(BasePlugin):
    meta = Meta(
        name="plugin_plan_supervisor",
        version="1.0",
        priority=2.9,  # Après planificateur, avant exécution
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        etape_courante = ctx.get("tache_courante", "")
        plugins_log = ctx.setdefault("plugins_log", [])

        if not plan:
            plugins_log.append("plugin_plan_supervisor : aucun plan détecté")
            return ctx

        terminées = [etape for etape in plan if etape["status"] == "fait"]
        en_cours = [etape for etape in plan if etape["status"] == "en cours"]
        à_faire = [etape for etape in plan if etape["status"] == "à faire"]

        if not en_cours and à_faire:
            # Redémarrage automatique de l'étape suivante
            prochaine = à_faire[0]["étape"]
            ctx["tache_courante"] = prochaine
            à_faire[0]["status"] = "en cours"
            plugins_log.append(f"plugin_plan_supervisor : redémarrage de l’étape → {prochaine}")
            logger.info(f"[plan_supervisor] Relance automatique de l’étape : {prochaine}")
        elif etape_courante and not any(e["étape"] == etape_courante for e in plan):
            plugins_log.append("plugin_plan_supervisor : étape courante non incluse dans le plan.")
            logger.warning(f"[plan_supervisor] Étape inconnue : {etape_courante}")

        return ctx
