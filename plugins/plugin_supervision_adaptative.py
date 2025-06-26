import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.supervision_adaptative")

class PluginSupervisionAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_supervision_adaptative",
        version="1.0",
        priority=9.5,  # Très tardif, en toute fin de cycle
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.setdefault("plugins_log", [])
        bilan = []

        erreurs = ctx.get("errors", [])
        intention = ctx.get("intention", "")
        plan = ctx.get("plan", [])
        tache = ctx.get("tache_courante", "")
        quota = ctx.get("user_quota", {}).get("req_used", 0)
        debug_mode = False

        # Supervision des erreurs
        if erreurs:
            bilan.append(f"⚠️ {len(erreurs)} erreur(s) détectée(s)")
            debug_mode = True

        # Supervision de l'intention
        if not intention or intention in ["vide", ""]:
            bilan.append("❓ Intention incertaine.")
            debug_mode = True

        # Supervision du plan
        if not plan:
            bilan.append("🚧 Aucun plan actif.")
        elif tache and all(e["status"] == "fait" for e in plan):
            bilan.append("✅ Plan complété.")
        else:
            bilan.append(f"🔄 Étape en cours : {tache}")

        # Quota
        if quota > 90:
            bilan.append("⛔ Quota proche du maximum.")
            debug_mode = True

        # Injection mode debug
        if debug_mode:
            ctx["debug_mode"] = True
            logs.append("plugin_supervision_adaptative : mode debug activé.")

        ctx["bilan_supervision"] = "\n".join(bilan)
        logs.append("plugin_supervision_adaptative : bilan injecté.")
        logger.info(f"[supervision] Bilan :\n{ctx['bilan_supervision']}")

        return ctx
