# plugins/plugin_goal_replanner.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.goal_replanner")

class PluginGoalReplanner(BasePlugin):
    meta = Meta(
        name="plugin_goal_replanner",
        version="1.0",
        priority=60.0,  # après planificateur dynamique, avant raisonneur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {})
        objectif_texte = objectif.get("but", "")
        if not objectif_texte:
            ctx.setdefault("plugins_log", []).append("PluginGoalReplanner : aucun objectif trouvé.")
            return ctx

        prompt = (
            f"Objectif actuel : « {objectif_texte} »\n"
            "Analyse si cet objectif est clair, pertinent et atteignable. "
            "Si non, propose une version reformulée ou améliorée. "
            "Sinon, confirme qu’il est optimal.\n\nRéponse :"
        )

        try:
            from plugins.utils.llm_call import call_llm_main
            suggestion = await call_llm_main(ctx, prompt)
            suggestion = suggestion.strip()

            if suggestion.lower().startswith("objectif optimal"):
                ctx.setdefault("plugins_log", []).append("PluginGoalReplanner : objectif confirmé.")
            else:
                ctx["objectif"]["but"] = suggestion
                ctx.setdefault("plugins_log", []).append("PluginGoalReplanner : objectif reformulé.")
        except Exception as e:
            logger.warning(f"[plugin_goal_replanner] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append(f"PluginGoalReplanner : erreur → {e}")

        return ctx
