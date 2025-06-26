"""
Plugin : coherence_cyclique
Rôle : Vérifier la cohérence de la réponse avec l'historique des réponses sur un même sujet
Priorité : 4.1 (après génération, juste avant affichage)
Auteur : AGI & Matthieu
"""

import logging
import os
import json
from difflib import SequenceMatcher
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.coherence_cyclique")

class CoherenceCycliquePlugin(BasePlugin):
    meta = Meta(
        name="coherence_cyclique",
        priority=4.1,
        version="1.0",
        author="AGI & Matthieu"
    )

    LOG_PATH = "coherence_log.json"
    SEUIL_SIMILARITE = 0.65

    def charger_log(self):
        if not os.path.exists(self.LOG_PATH):
            return []
        try:
            with open(self.LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def enregistrer_log(self, entry):
        historique = self.charger_log()
        historique.append(entry)
        with open(self.LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(historique, f, indent=2, ensure_ascii=False)

    def similarite(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        reponse = ctx.get("llm_response", "")

        if not message or not reponse:
            plugins_log.append("CoherenceCycliquePlugin : message ou réponse manquant.")
            return ctx

        historique = self.charger_log()
        similitudes = [
            (self.similarite(message, h["message"]), h)
            for h in historique if "message" in h and "reponse" in h
        ]
        similitudes_pertinentes = sorted(
            [x for x in similitudes if x[0] >= self.SEUIL_SIMILARITE],
            key=lambda x: -x[0]
        )

        if similitudes_pertinentes:
            derniere = similitudes_pertinentes[0][1]
            score = self.similarite(reponse, derniere["reponse"])
            if score < 0.5:
                ctx["alerte_coherence"] = f"⚠️ Réponse peut-être incohérente avec un ancien échange (similarité faible : {int(score*100)}%)"
                plugins_log.append("CoherenceCycliquePlugin : incohérence potentielle détectée.")
                logger.warning(f"[coherence_cyclique] Alerte incohérence - Similarité réponse : {score:.2f}")
            else:
                plugins_log.append("CoherenceCycliquePlugin : cohérence conservée.")
        else:
            plugins_log.append("CoherenceCycliquePlugin : aucun historique comparable.")

        self.enregistrer_log({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "reponse": reponse
        })

        return ctx
