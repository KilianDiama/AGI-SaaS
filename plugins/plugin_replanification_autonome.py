# plugins/plugin_replanification_autonome.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.replanification_autonome")

class PluginReplanificationAutonome(BasePlugin):
    meta = Meta(
        name="plugin_replanification_autonome",
        version="1.0",
        priority=98.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        note = ctx.get("evaluation_reponse", {}).get("note", 5)
        alignement = ctx.get("alignment_score", 1)
        step_status = ctx.get("plan_restantes", [])
        erreurs = ctx.get("errors", [])
        retry = False

        # Détection échec stratégique
        if note <= 2 or alignement < 0.5 or len(erreurs) > 0:
            retry = True

        if retry:
            # 🔁 Replanification
            ancien_plan = ctx.get("plan", [])
            nouveau_plan = [
                {"étape": "réévaluer le besoin", "status": "à faire"},
                {"étape": "formuler une nouvelle stratégie", "status": "à faire"},
                {"étape": "implémenter l’approche", "status": "à faire"}
            ]
            ctx["plan"] = nouveau_plan
            ctx["tache_courante"] = "réévaluer le besoin"
            ctx.setdefault("plugins_log", []).append("PluginReplanificationAutonome : plan relancé ✅")
        else:
            ctx.setdefault("plugins_log", []).append("PluginReplanificationAutonome : plan maintenu")

        return ctx
