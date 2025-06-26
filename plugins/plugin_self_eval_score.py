import logging
from noyau_core import BasePlugin, Context, Meta
import random

logger = logging.getLogger("plugin.self_eval_score")

class PluginSelfEvalScore(BasePlugin):
    meta = Meta(
        name="plugin_self_eval_score",
        version="1.0",
        priority=9.1,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("response", "") or ctx.get("llm_response", "")

        if not response.strip():
            ctx["self_eval_score"] = {
                "note": 0,
                "verdict": "Pas de réponse à évaluer.",
                "feedback": "Réponse vide ou absente."
            }
            ctx.setdefault("plugins_log", []).append("PluginSelfEvalScore : réponse vide, note 0")
            return ctx

        # Analyse basique des critères (longueur, structure, contenu, tonalité, clarté)
        longueur = len(response)
        clarté = 1 if "." in response and longueur > 40 else 0
        structure = 1 if "\n" in response else 0
        confiance = random.uniform(0.7, 0.95)

        note = round((clarté + structure + confiance) * 3.5, 2)

        verdict = (
            "Réponse bien structurée, claire et fluide."
            if note > 7
            else "Réponse partiellement claire, améliorable."
        )

        ctx["self_eval_score"] = {
            "note": note,
            "verdict": verdict,
            "feedback": f"Note générée selon critères simples : longueur={longueur}, clarté={clarté}, structure={structure}, confiance≈{round(confiance, 2)}"
        }

        ctx.setdefault("plugins_log", []).append(f"PluginSelfEvalScore : note auto-évaluée = {note}")
        logger.info(f"[self_eval_score] Évaluation → note {note}, verdict : {verdict}")

        return ctx
