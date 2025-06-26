"""
Plugin : simulation_decisionnelle
Rôle : Simuler plusieurs options de décision, comparer leur qualité, et choisir la plus pertinente
Priorité : 2.5 (juste avant la génération finale ou appel LLM)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.simulation_decisionnelle")

class SimulationDecisionnellePlugin(BasePlugin):
    meta = Meta(
        name="simulation_decisionnelle",
        priority=2.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectifs = ctx.get("objectifs_actifs", {})
        message = ctx.get("message", "")

        # Idées simulées naïvement (exemples fictifs ici)
        options = [
            {"id": "rapide", "reponse": "Voici une réponse directe.", "poids": objectifs.get("rapidité", 0)},
            {"id": "fiable", "reponse": "D’après mes sources internes, la réponse la plus cohérente est…", "poids": objectifs.get("fiabilité", 0)},
            {"id": "creatif", "reponse": "Et si on imaginait ceci ?...", "poids": objectifs.get("créativité", 0)}
        ]

        meilleure = max(options, key=lambda opt: opt["poids"])
        ctx["llm_response"] = meilleure["reponse"]
        ctx["decision_simulee"] = meilleure["id"]

        plugins_log.append(f"SimulationDecisionnellePlugin : réponse simulée choisie → {meilleure['id']}")
        logger.info(f"[simulation_decisionnelle] Option gagnante : {meilleure['id']}")

        return ctx
