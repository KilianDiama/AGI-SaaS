"""
Plugin : projection_alternative
Rôle : Simuler plusieurs évolutions mentales possibles à partir d’un même état
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.projection_alternative")

class ProjectionAlternativePlugin(BasePlugin):
    meta = Meta(
        name="projection_alternative",
        priority=6,
        version="1.1",  # ← version sécurisée
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Sécurité : objectif
        objectif = ctx.get("objectif", {})
        if not isinstance(objectif, dict):
            objectif = {}
        but = str(objectif.get("but", "non défini"))

        # Sécurité : historique
        historique_evolution = ctx.get("historique_evolution", [])
        if not isinstance(historique_evolution, list):
            historique_evolution = []
        cycle_id = len(historique_evolution)

        if not but or but == "non défini":
            ctx["projection_alternative"] = "❌ Aucun objectif à extrapoler."
            plugins_log.append("ProjectionAlternativePlugin : rien à simuler")
            return ctx

        scenarios = [
            {
                "titre": "🔁 Recombinaison interne",
                "description": f"Si je reçois à nouveau le même type d’objectif ({but}), je pourrais combiner mes anciens modules pour le résoudre différemment."
            },
            {
                "titre": "📚 Expansion mémorielle",
                "description": "Je commence à dépendre plus fortement de ma mémoire experientielle, ce qui transforme mes cycles en apprentissage progressif."
            },
            {
                "titre": "🧭 Redirection identitaire",
                "description": f"Je change de but pour explorer une alternative plus éthique, plus efficace ou plus personnelle à '{but}'."
            }
        ]

        choix = random.choice(scenarios) if scenarios else {"titre": "❓ Aucun scénario", "description": "Aucun scénario disponible."}

        ctx["projection_alternative"] = {
            "cycle": cycle_id,
            "futurs_possibles": scenarios,
            "scenario_choisi": choix
        }

        plugins_log.append("ProjectionAlternativePlugin : scénarios simulés")
        logger.info("[projection_alternative] Futur sélectionné : " + choix["titre"])

        return ctx
