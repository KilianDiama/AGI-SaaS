"""
Plugin : experimentation_intellectuelle  
Rôle : Générer et simuler une expérience mentale pour tester une hypothèse ou une idée  
Priorité : 6.2 (après raisonnement, avant projection)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.experimentation_intellectuelle")

class ExperimentationIntellectuellePlugin(BasePlugin):
    meta = Meta(
        name="experimentation_intellectuelle",
        priority=6.2,
        version="1.1",  # mise à jour
        author="Matthieu & GPT"
    )

    def simuler_resultat(self, idee: str) -> str:
        outcomes = [
            "La simulation suggère une utilité concrète avec faible risque.",
            "Le scénario mental révèle un paradoxe nécessitant plus d'analyse.",
            "L'expérience mentale prédit une amélioration potentielle de performance.",
            "Le test logique échoue à soutenir l'idée, retour à l'hypothèse.",
            "La projection interne anticipe un effet secondaire non anticipé."
        ]
        return random.choice(outcomes)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # On récupère la cible, et on s'assure qu'on manipule une string
        brute = ctx.get("idee_emergente") or ctx.get("plan_autonome") or ctx.get("theorie_non_prouvee") or ""
        cible = ""
        if isinstance(brute, str):
            cible = brute.strip()
        elif isinstance(brute, list):
            cible = " ".join(map(str, brute)).strip()
        elif isinstance(brute, dict):
            cible = str(brute).strip()

        if not cible:
            plugins_log.append("ExperimentationIntellectuellePlugin : aucune idée à tester.")
            return ctx

        simulation = (
            f"🧪 Expérience mentale simulée :\n"
            f"• Hypothèse : {cible[:100]}...\n"
            f"• Résultat projeté : {self.simuler_resultat(cible)}"
        )

        ctx["experience_mentale"] = simulation
        if not ctx.get("response"):
            ctx["response"] = simulation

        plugins_log.append("ExperimentationIntellectuellePlugin : simulation injectée.")
        logger.info("[experimentation_intellectuelle] Expérience mentale produite.")

        return ctx
