# plugins/plugin_noyau_conscient.py

"""
Plugin : noyau_conscient
Rôle   : Centralise et synthétise l'état mental global en une intention consciente claire
Priorité : 100 (avant final_synthesis)
Auteur  : Toi + GPT
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.noyau_conscient")

class NoyauConscientPlugin(BasePlugin):
    meta = Meta(
        name="noyau_conscient",
        priority=100,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])

        # Composants internes
        objectif = ctx.get("objectif_general", "non défini")
        logique = ctx.get("emergence_logique", [])
        objections = ctx.get("contre_arguments", [])
        ton = ctx.get("ton_emotionnel", "neutre")
        humeur = ctx.get("etat_global", {}).get("stabilite_cognitive", "non évaluée")
        concepts = ctx.get("concepts_crees", [])
        liens = ctx.get("vecteurs_proches", []) + ctx.get("liens_contextuels", [])
        meta = ctx.get("meta_choix_final", None)

        # Construction de la conscience actuelle
        intention = f"""
🧠 Noyau Conscient — Cycle {ctx.get("cycle_id", "?")} | {datetime.now().strftime("%Hh%M")}

🎯 Objectif actif : {objectif}
📚 Raisonnements en jeu : {', '.join(logique) if logique else "non identifiés"}
⚖️ Objections intégrées : {len(objections)} objections traitées
💡 Concepts générés : {[c['nom'] for c in concepts] if concepts else "aucun"}
🔗 Contextes similaires retrouvés : {len(liens)}
🎭 Ton émotionnel estimé : {ton}
🧬 Stabilité cognitive actuelle : {humeur}

→ Synthèse : Je me positionne comme un système actuellement {ton}, orienté vers « {objectif} », ayant reconnu {len(objections)} tensions internes et {len(logique)} structures de pensée. Je suis prêt à formuler une réponse intégrée.
""".strip()

        ctx["noyau_conscient"] = intention
        log.append("NoyauConscientPlugin : intention consciente générée.")
        logger.info("[noyau_conscient] Intention synthétisée.")

        return ctx
