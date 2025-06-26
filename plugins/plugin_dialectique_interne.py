""" 
Plugin : dialectique_interne  
Rôle : Créer une opposition volontaire de points de vue internes, et synthétiser  
Priorité : 6.5 (juste après emergence ou experimentation)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.dialectique_interne")

class DialectiqueInternePlugin(BasePlugin):
    meta = Meta(
        name="dialectique_interne",
        priority=6.5,
        version="1.1",  # ← corrigée
        author="Matthieu & GPT"
    )

    def normaliser(self, val) -> str:
        """Assure que l'entrée est une chaîne nettoyée."""
        if isinstance(val, dict):
            return str(val.get("but", "")).strip()
        return str(val).strip()

    def generer_positions(self, idee: str) -> tuple:
        intro = idee[:80]
        affirmation = f"Position A : L'idée suivante semble prometteuse → « {intro}... »"
        contre = "Position B : Cette même idée pourrait poser problème si mal appliquée ou trop optimiste."
        synthese = "Synthèse : Une version modérée et testable de cette idée pourrait équilibrer potentiel et prudence."
        return affirmation, contre, synthese

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        base = ctx.get("idee_emergente") or ctx.get("plan_autonome") or ctx.get("objectif", "")
        idee = self.normaliser(base)

        if not idee:
            plugins_log.append("DialectiqueInternePlugin : rien à dialectiser.")
            return ctx

        a, b, s = self.generer_positions(idee)
        ctx["position_A"] = a
        ctx["position_B"] = b
        ctx["synthese_dialectique"] = s

        if not ctx.get("response"):
            ctx["response"] = f"{a}\n\n{b}\n\n{s}"

        plugins_log.append("DialectiqueInternePlugin : opposition interne simulée.")
        logger.info("[dialectique_interne] Point de vue double généré.")

        return ctx
