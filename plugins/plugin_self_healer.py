# plugins/plugin_self_healer.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.self_healer")

class PluginSelfHealer(BasePlugin):
    meta = Meta(
        name="plugin_self_healer",
        version="1.0",
        priority=98.1,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        conscience = ctx.get("conscience_iterative", {}).get("analyse", {})
        reponse = ctx.get("llm_response", "")
        plan = ctx.get("plan", [])

        should_retry = (
            conscience.get("réponse_vide") or
            conscience.get("réponse_confuse") or
            conscience.get("étapes_incomplètes")
        )

        if should_retry:
            ctx["llm_prompt"] = ctx.get("llm_prompt") + "\n\n# ⚠️ Améliore ta réponse précédente. Elle était trop faible ou incomplète."
            ctx["llm_response"] = ""
            ctx["plan"] = [etape | {"status": "à refaire"} if etape["status"] != "terminé" else etape for etape in plan]
            ctx.setdefault("plugins_log", []).append("PluginSelfHealer : réponse jugée faible, déclenchement relance.")
        else:
            ctx.setdefault("plugins_log", []).append("PluginSelfHealer : réponse jugée suffisante, aucune action.")

        return ctx
