import logging
from typing import Dict
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.response_evaluator_plus")

class PluginResponseEvaluatorPlus(BasePlugin):
    meta = Meta(
        name="plugin_response_evaluator_plus",
        version="1.0",
        priority=4.8,  # Avant réponse finale et dashboard
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("response", "").strip()
        message = ctx.get("message", "").strip().lower()
        intention = ctx.get("intention", "").strip().lower()
        plugins_log = ctx.setdefault("plugins_log", [])

        if not response:
            ctx["evaluation_plus"] = {
                "pertinence": 0.0,
                "clarté": 0.0,
                "créativité": 0.0,
                "alignement_intention": 0.0,
                "utilité": 0.0,
                "note_globale": 0.0
            }
            plugins_log.append("plugin_response_evaluator_plus : réponse vide → note 0")
            return ctx

        scores: Dict[str, float] = {
            "pertinence": 1.5 if message in response.lower() else 1.0,
            "clarté": 1.0 + (0.5 if len(response.split(".")) > 2 else 0.0),
            "créativité": 1.0 + (0.5 if "!" in response or "imaginons" in response else 0.0),
            "alignement_intention": 1.0 + (0.5 if intention in response.lower() else 0.0),
            "utilité": 1.0 + (0.5 if "tu peux" in response or "voici" in response else 0.0)
        }

        note = sum(scores.values()) / len(scores)

        ctx["evaluation_plus"] = {
            **scores,
            "note_globale": round(note, 2)
        }

        plugins_log.append(f"plugin_response_evaluator_plus : note = {note:.2f}")
        logger.info(f"[evaluator_plus] Évaluation complète : {ctx['evaluation_plus']}")

        return ctx
