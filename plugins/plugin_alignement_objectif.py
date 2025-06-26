# plugins/plugin_alignement_objectif.py

import re
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.alignement_objectif")


class PluginAlignementObjectif(BasePlugin):
    meta = Meta(
        name="plugin_alignement_objectif",
        priority=2.7,  # juste après analyse_feedback, avant raisonneur
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.seuil_alignement = 0.35  # Seuil minimal pour un alignement considéré comme suffisant

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "")
        reponse = ctx.get("response", "")

        resultat = self.analyser(objectif, reponse)
        ctx["alignement_objectif"] = resultat

        log = f"PluginAlignementObjectif : {resultat['verdict']} ({resultat['alignement']*100:.1f}%)"
        ctx.setdefault("plugins_log", []).append(log)
        logger.info(log)

        return ctx

    def evaluer_alignement(self, objectif: str, reponse: str) -> float:
        if not objectif or not reponse:
            return 0.0

        mots_obj = set(re.findall(r'\b\w+\b', objectif.lower()))
        mots_rep = set(re.findall(r'\b\w+\b', reponse.lower()))

        if not mots_obj:
            return 0.0

        mots_communs = mots_obj & mots_rep
        score = len(mots_communs) / len(mots_obj)

        return round(score, 4)

    def analyser(self, objectif: str, reponse: str) -> dict:
        score = self.evaluer_alignement(objectif, reponse)
        messages = []

        if score >= self.seuil_alignement:
            messages.append(f"✅ Alignement suffisant ({score*100:.1f}%) entre l'objectif et la réponse.")
            verdict = "aligné"
        else:
            messages.append(f"⚠️ Alignement insuffisant ({score*100:.1f}%) entre l'objectif et la réponse.")
            verdict = "non aligné"

        return {
            "alignement": score,
            "messages": messages,
            "verdict": verdict
        }
