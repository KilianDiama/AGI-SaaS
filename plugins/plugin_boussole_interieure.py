""" 
Plugin : boussole_interieure  
Rôle : Évaluer et prioriser les objectifs cognitifs pour guider la concentration du système  
Priorité : 5.9 (avant réponse ou projection)  
Auteur : Matthieu & GPT  
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.boussole_interieure")

class BoussoleInterieurePlugin(BasePlugin):
    meta = Meta(
        name="boussole_interieure",
        priority=5.9,
        version="1.1",  # ← version corrigée
        author="Matthieu & GPT"
    )

    def evaluer(self, texte: str) -> dict:
        score_valeur = 40 + (len(texte) % 30)
        score_urgence = 30 + (len(texte) % 20)
        score_nouveaute = 10 + (len(set(texte)) % 20)
        return {
            "valeur": score_valeur,
            "urgence": score_urgence,
            "nouveauté": score_nouveaute,
            "total": score_valeur + score_urgence + score_nouveaute
        }

    def normaliser(self, x) -> str:
        if isinstance(x, dict):
            return str(x.get("but", "")).strip()
        return str(x).strip()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        candidats_raw = {
            "actuel": ctx.get("objectif", ""),
            "suivant": ctx.get("objectif_autonome_suivant", ""),
            "mission": ctx.get("objectifs_long_terme", "")
        }

        evaluations = {}
        for nom, val in candidats_raw.items():
            texte = self.normaliser(val)
            if not texte:
                continue
            score = self.evaluer(texte)
            evaluations[nom] = {
                "objectif": texte[:120],
                "scores": score
            }

        if not evaluations:
            plugins_log.append("BoussoleInterieurePlugin : rien à prioriser.")
            return ctx

        tri = sorted(evaluations.items(), key=lambda kv: kv[1]["scores"]["total"], reverse=True)
        ctx["priorisation_objectifs"] = tri

        plugins_log.append(f"BoussoleInterieurePlugin : objectif prioritaire → {tri[0][0]}")
        logger.info("[boussole_interieure] Classement des objectifs terminé.")

        return ctx
