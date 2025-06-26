"""
Plugin : auto_critique
Rôle : Évaluer la qualité logique et utile de la réponse générée (méta-analyse)
Priorité : 4.9 (après génération, juste avant affichage ou action)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.auto_critique")

class AutoCritiquePlugin(BasePlugin):
    meta = Meta(
        name="auto_critique",
        priority=4.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    def evaluer(self, reponse: str) -> dict:
        note = 1.0
        raisons = []

        if not reponse or len(reponse.strip()) < 5:
            note = 0.0
            raisons.append("Réponse vide ou insuffisante.")
        elif len(reponse.strip()) < 25:
            note = 0.3
            raisons.append("Réponse trop courte.")
        if "je ne sais pas" in reponse.lower():
            note -= 0.4
            raisons.append("Manque d'effort ou incertitude.")
        if any(w in reponse.lower() for w in ["erreur", "confus", "pas clair"]):
            note -= 0.3
            raisons.append("Réponse perçue comme confuse.")

        return {
            "note": max(0.0, min(1.0, round(note, 2))),
            "raisons": raisons or ["Réponse acceptable."]
        }

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        if not reponse:
            plugins_log.append("AutoCritiquePlugin : rien à évaluer.")
            return ctx

        critique = self.evaluer(reponse)
        ctx["eval_plugin_propose"] = critique

        log_msg = f"AutoCritiquePlugin : note = {critique['note']} / Raisons : {', '.join(critique['raisons'])}"
        plugins_log.append(log_msg)
        logger.info(f"[auto_critique] {log_msg}")

        return ctx
