"""
Plugin : analyse_comparative
Rôle : Comparer les réponses des LLMs utilisés et évaluer la réponse la plus cohérente
Priorité : 3.1 (juste après génération multi-LLM, avant fusion ou sélection finale)
Auteur : AGI & Matthieu
"""

import logging
from difflib import SequenceMatcher
from statistics import mean
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.analyse_comparative")

class AnalyseComparativePlugin(BasePlugin):
    meta = Meta(
        name="analyse_comparative",
        priority=3.1,
        version="1.0",
        author="AGI & Matthieu"
    )

    def similarite(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a.strip().lower(), b.strip().lower()).ratio()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponses = ctx.get("llm_responses", [])

        if not reponses or len(reponses) < 2:
            plugins_log.append("AnalyseComparativePlugin : pas assez de réponses pour comparer.")
            return ctx

        similarites = []
        for i in range(len(reponses)):
            for j in range(i + 1, len(reponses)):
                s = self.similarite(reponses[i], reponses[j])
                similarites.append(s)

        moyenne = mean(similarites) if similarites else 0
        ctx["comparaison_llm_score"] = moyenne
        plugins_log.append(f"AnalyseComparativePlugin : score moyen de similarité LLM = {moyenne:.2f}")
        logger.info(f"[analyse_comparative] Similarité moyenne : {moyenne:.2f}")

        return ctx
