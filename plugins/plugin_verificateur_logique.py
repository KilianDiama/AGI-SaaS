# plugins/plugin_verificateur_logique.py

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.verificateur_logique")

class PluginVerificateurLogique(BasePlugin):
    meta = Meta(
        name="plugin_verificateur_logique",
        priority=3.4,  # Après raisonneur, avant vote
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        réponse = ctx.get("llm_response", "")
        note = 0.0
        verdict = ""

        if not réponse.strip():
            note = 0
            verdict = "vide"
        elif self._contradiction_detectée(réponse):
            note = 1
            verdict = "contradictoire"
        elif self._trop_général(réponse):
            note = 2
            verdict = "trop vague"
        else:
            note = 4
            verdict = "valide"

        ctx["evaluation_reponse"] = {
            "verdict": verdict,
            "note": note,
            "longueur": len(réponse)
        }

        ctx.setdefault("plugins_log", []).append(
            f"PluginVerificateurLogique : évaluation = {verdict} (note {note})"
        )

        logger.info(f"[verificateur_logique] Verdict = {verdict} | Note = {note}")
        return ctx

    def _contradiction_detectée(self, texte: str) -> bool:
        patterns = [
            r"\b(c'est vrai|c'est faux)\b.*\b(c'est faux|c'est vrai)\b",
            r"\bje ne sais pas\b.*\bmais\b.*\bje suis sûr\b",
        ]
        return any(re.search(p, texte, re.IGNORECASE | re.DOTALL) for p in patterns)

    def _trop_général(self, texte: str) -> bool:
        trop_vagues = ["ça dépend", "c'est possible", "on peut dire que", "d’une certaine manière"]
        return any(vague in texte.lower() for vague in trop_vagues)
