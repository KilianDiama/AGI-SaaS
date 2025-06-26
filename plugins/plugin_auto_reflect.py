# plugins/plugin_auto_reflect.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.auto_reflect")

class PluginAutoReflect(BasePlugin):
    meta = Meta(
        name="plugin_auto_reflect",
        version="1.0",
        priority=105.0,  # Après raisonnement + vérificateurs
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("response", "").strip()
        objectif = ctx.get("objectif_actuel", "")
        score = ctx.get("evaluation_reponse", {}).get("note", 0)

        if not response:
            ctx.setdefault("plugins_log", []).append("PluginAutoReflect : réponse vide, relance nécessaire.")
            ctx["relancer_cycle"] = True
            return ctx

        if score < 2.5:
            critique = f"Réponse jugée insuffisante (note={score}). Nouvelle tentative recommandée."
            ctx["relancer_cycle"] = True
            ctx.setdefault("plugins_log", []).append(f"PluginAutoReflect : {critique}")
            ctx["critique_llm"] = critique
        else:
            ctx.setdefault("plugins_log", []).append(f"PluginAutoReflect : réponse jugée acceptable (note={score}).")

        return ctx
