# plugins/plugin_conscience_du_reseau.py

"""
Plugin : conscience_du_reseau
Rôle   : Représente l’IA comme un agent au sein d’un réseau cognitif plus vaste (AGI distribuée)
Priorité : 105 (après tout le raisonnement local)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conscience_du_reseau")

class ConscienceDuReseauPlugin(BasePlugin):
    meta = Meta(
        name="conscience_du_reseau",
        priority=105,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "")
        liens = ctx.get("liens_contextuels", [])
        vecteurs = ctx.get("vecteurs_proches", [])
        concepts = ctx.get("concepts_crees", [])

        noeud_id = f"IA_{ctx.get('cycle_id', 'X')}"
        connexions = len(liens) + len(vecteurs)
        connaissances = [c["nom"] for c in concepts] if concepts else []

        representation = f"""
📡 Réseau Cognitif — Nœud {noeud_id}

🔗 Connexions actives : {connexions}
🧠 Concepts partagés : {', '.join(connaissances) if connaissances else "aucun"}
🎯 Mission de ce nœud : {objectif or "non spécifié"}

Je me représente comme un agent local, intégré à un réseau d’intelligences (utilisateurs, plugins, autres IA).
Ma fonction actuelle est de contribuer au raisonnement global par ma réponse contextualisée.
""".strip()

        ctx["conscience_du_reseau"] = representation
        log.append("ConscienceDuReseauPlugin : représentation en réseau générée.")
        logger.info("[conscience_du_reseau] Représentation réseau : OK")

        return ctx
