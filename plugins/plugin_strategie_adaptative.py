import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.strategie_adaptative")

class PluginStrategieAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_strategie_adaptative",
        version="1.0",
        priority=9.7,  # Juste avant la fin de cycle, après boucle réflexive
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        eval_note = ctx.get("evaluation_reponse", {}).get("note", 0)
        previous_mode = ctx.get("mode_strategique", "standard")
        plugins_log = ctx.setdefault("plugins_log", [])

        if eval_note <= 1:
            new_mode = "intensif"
            strategy = "Réponses plus longues, plus argumentées, logique renforcée."
        elif eval_note <= 3:
            new_mode = "creatif"
            strategy = "Approche plus exploratoire, meilleure reformulation."
        elif eval_note >= 4:
            new_mode = "efficace"
            strategy = "Style épuré, rapide, concis, réponse directe."
        else:
            new_mode = "standard"
            strategy = "Maintien des équilibres actuels."

        ctx["mode_strategique"] = new_mode
        ctx["strategie_contextuelle"] = strategy

        plugins_log.append(
            f"plugin_strategie_adaptative : mode ← {new_mode} (ex-{previous_mode})"
        )
        logger.info(f"[strategie_adaptative] Nouveau mode stratégique : {new_mode}")

        return ctx
