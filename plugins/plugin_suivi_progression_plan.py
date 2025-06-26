from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.suivi_progression")

class PluginSuiviProgressionPlan(BasePlugin):
    meta = Meta(
        name="plugin_suivi_progression_plan",
        version="1.0",
        priority=1.6,  # Après planificateur et raisonneur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        etape_actuelle = ctx.get("tache_courante", "")
        message_utilisateur = ctx.get("message", "").strip()

        if not plan or not etape_actuelle:
            ctx.setdefault("plugins_log", []).append("plugin_suivi_progression_plan : plan ou tâche manquant")
            return ctx

        # Simule validation de l'étape si un message a été traité
        for étape in plan:
            if étape["étape"] == etape_actuelle:
                if étape["status"] != "fait" and message_utilisateur:
                    étape["status"] = "fait"
                    ctx.setdefault("plugins_log", []).append(f"plugin_suivi_progression_plan : étape '{etape_actuelle}' marquée faite")
                    logger.info(f"[progression] Étape complétée : {etape_actuelle}")
                break

        # Passage à la prochaine étape
        prochaines = [e for e in plan if e["status"] != "fait"]
        ctx["tache_courante"] = prochaines[0]["étape"] if prochaines else None

        if not prochaines:
            ctx.setdefault("plugins_log", []).append("plugin_suivi_progression_plan : plan terminé")
        else:
            ctx.setdefault("plugins_log", []).append(f"plugin_suivi_progression_plan : prochaine étape → {ctx['tache_courante']}")

        return ctx
