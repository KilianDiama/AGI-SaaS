from noyau_core import BasePlugin, Context, Meta
from textstat import flesch_reading_ease, flesch_kincaid_grade
import logging

logger = logging.getLogger("plugin.evaluation_qualite")

class PluginEvaluationQualite(BasePlugin):
    meta = Meta(
        name="plugin_evaluation_qualite",
        version="1.0",
        priority=4.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("llm_response", "") or ctx.get("response", "")
        if not texte.strip():
            ctx.setdefault("plugins_log", []).append("PluginEvaluationQualite : texte vide")
            ctx["evaluation_reponse"] = {"verdict": "vide", "note": 0, "longueur": 0}
            return ctx

        longueur = len(texte)
        lisibilite = flesch_reading_ease(texte)
        grade = flesch_kincaid_grade(texte)

        note = round((lisibilite + 100 - grade * 10) / 2, 2)
        verdict = "excellente" if note > 70 else "moyenne" if note > 50 else "faible"

        ctx["evaluation_reponse"] = {
            "verdict": verdict,
            "note": note,
            "longueur": longueur
        }

        ctx.setdefault("plugins_log", []).append(
            f"PluginEvaluationQualite : {verdict} (note={note}, longueur={longueur})"
        )
        logger.info(f"[éval qualité] {verdict} - note: {note}, len: {longueur}")

        return ctx
