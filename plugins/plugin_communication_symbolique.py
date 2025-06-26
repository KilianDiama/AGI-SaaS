# plugins/plugin_communication_symbolique.py

"""
Plugin : communication_symbolique
Rôle   : Exprime les raisonnements internes sous forme de métaphores, analogies, ou images symboliques
Priorité : 93 (après emergence_logique, avant finalisation)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.communication_symbolique")

class CommunicationSymboliquePlugin(BasePlugin):
    meta = Meta(
        name="communication_symbolique",
        priority=93,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        concepts = ctx.get("emergence_logique", [])
        objections = ctx.get("contre_arguments", [])
        ton = ctx.get("ton_emotionnel", "neutre")

        symboles = []

        for c in concepts:
            if "inférence" in c:
                symboles.append("🧩 Une pièce de puzzle logique vient de s’emboîter.")
            if "hypothèse" in c:
                symboles.append("🌱 Une idée est plantée, en attente de validation.")
            if "recommandation" in c:
                symboles.append("📌 Une boussole morale pointe vers une direction préférable.")
        
        for o in objections:
            if "absolus" in o:
                symboles.append("⚖️ Le discours tremble sur ses fondations rigides.")
            if "manque de nuance" in o:
                symboles.append("🌫️ Le brouillard du doute demande clarté.")

        if not symboles:
            symboles.append("🌀 Aucune figure symbolique détectée.")

        ctx["symboles_expressifs"] = symboles
        log.append(f"CommunicationSymboliquePlugin : {len(symboles)} images mentales générées.")
        logger.info(f"[communication_symbolique] Symboles = {symboles}")

        return ctx
