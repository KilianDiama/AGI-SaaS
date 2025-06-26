# plugins/plugin_relation_contextuelle.py

"""
Plugin : relation_contextuelle
Rôle   : Détecte des liens implicites entre le contexte actuel et des cycles passés (mémorisation associative)
Priorité : -25 (avant le raisonnement)
Auteur  : Toi + GPT
"""

import logging
from difflib import SequenceMatcher
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.relation_contextuelle")

class RelationContextuellePlugin(BasePlugin):
    meta = Meta(
        name="relation_contextuelle",
        priority=-25,
        version="1.0",
        author="Toi + GPT"
    )

    # Simule une mémoire contextuelle persistante
    historique_cycles = []

    def similarite(self, a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").lower()
        liens = []

        # Compare avec mémoire
        for cycle in RelationContextuellePlugin.historique_cycles[-30:]:
            similarite = self.similarite(cycle["message"], message)
            if similarite > 0.5:
                liens.append({
                    "cycle_id": cycle["cycle_id"],
                    "message_ancien": cycle["message"],
                    "similarite": round(similarite, 2)
                })

        # Stocke le lien
        ctx["liens_contextuels"] = liens

        # Ajoute ce cycle à la mémoire
        RelationContextuellePlugin.historique_cycles.append({
            "cycle_id": ctx.get("cycle_id"),
            "message": message
        })

        if liens:
            log.append(f"RelationContextuellePlugin : {len(liens)} contextes liés détectés.")
            logger.info(f"[relation_contextuelle] Liens : {liens}")
        else:
            log.append("RelationContextuellePlugin : aucun lien contextuel détecté.")

        return ctx
