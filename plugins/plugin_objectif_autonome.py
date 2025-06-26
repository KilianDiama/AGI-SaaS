# plugins/plugin_objectif_autonome.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.objectif_autonome")

class PluginObjectifAutonome(BasePlugin):
    meta = Meta(
        name="plugin_objectif_autonome",
        version="1.0",
        priority=2.1,  # avant planification
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip()
        message = ctx.get("message", "").strip()
        intention = ctx.get("intention", "non détectée")

        if objectif or not message:
            ctx.setdefault("plugins_log", []).append("ObjectifAutonome : pas d’objectif généré.")
            return ctx

        prompt = f"""Tu es un assistant de planification intelligente.
Analyse ce message et déduis un objectif clair, opérationnel et réaliste.

Message utilisateur :
---
{message}
---

Donne-moi uniquement l’objectif sous forme d’une phrase claire, sans intro ni conclusion.
"""
        from plugins.utils.llm_call import call_llm_main
        objectif_deduit = (await call_llm_main(ctx, prompt)).strip()

        if objectif_deduit:
            ctx["objectif"] = {"but": objectif_deduit, "état": "en cours", "priorité": 1}
            ctx.setdefault("plugins_log", []).append(f"ObjectifAutonome : objectif généré → {objectif_deduit}")
        else:
            ctx.setdefault("plugins_log", []).append("ObjectifAutonome : échec génération objectif")

        return ctx
