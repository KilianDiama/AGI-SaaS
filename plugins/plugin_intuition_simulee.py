"""
Plugin : intuition_simulee
Rôle : Générer une hypothèse initiale non argumentée comme point de départ spontané
Priorité : 2.8 (très tôt dans le cycle cognitif)
Auteur : Matthieu & GPT
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.intuition_simulee")

class IntuitionSimuleePlugin(BasePlugin):
    meta = Meta(
        name="intuition_simulee",
        priority=2.8,
        version="1.2",  # ← mise à jour
        author="Matthieu & GPT"
    )

    amorces = [
        "🔮 Je ressens que la clef se trouve peut-être ici : ",
        "🌀 Mon instinct me pousse vers : ",
        "🌫️ Il y a comme une évidence diffuse : ",
        "✨ Avant toute analyse, je pressens : ",
        "🌱 Quelque chose me dit de considérer : "
    ]

    def intuition_expressive(self, objectif: str) -> str:
        base = objectif.strip()[:80] or "une possibilité émergente"
        intro = random.choice(self.amorces)
        return f"{intro}{base}..."

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif", "")

        # Sécurité : convertir en str
        if not isinstance(objectif, str):
            objectif = str(objectif)
        objectif = objectif.strip()

        if not objectif:
            plugins_log.append("IntuitionSimuleePlugin : 🚫 aucun objectif à pressentir.")
            logger.info("[intuition_simulee] Aucun objectif présent, plugin ignoré.")
            return ctx

        intuition = self.intuition_expressive(objectif)
        ctx["intuition"] = intuition

        if not ctx.get("response"):
            ctx["response"] = f"{intuition}"

        plugins_log.append("IntuitionSimuleePlugin : 💡 hypothèse intuitive générée.")
        logger.info(f"[intuition_simulee] Intuition produite : {intuition}")

        return ctx
