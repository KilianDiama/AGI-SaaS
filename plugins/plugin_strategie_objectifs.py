"""
Plugin : strategie_objectifs
Rôle : Décomposer un objectif complexe en sous-objectifs stratégiques
Priorité : 2.5 (entre perception et réflexion interne)
Auteur : Matthieu & GPT
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.strategie_objectifs")

class StrategieObjectifsPlugin(BasePlugin):
    meta = Meta(
        name="strategie_objectifs",
        priority=2.5,
        version="1.2",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    def generer_sous_objectifs(self, objectif_principal: str) -> list:
        base = objectif_principal.strip()
        if not base:
            return []

        modèles = [
            f"✔ Comprendre les implications de « {base} »",
            f"🔍 Identifier les ressources nécessaires à « {base} »",
            f"🛠️ Définir les étapes intermédiaires vers « {base} »",
            f"⚖️ Évaluer les risques liés à « {base} »",
            f"🧭 Proposer un plan d'action structuré pour « {base} »",
            f"📊 Déterminer des indicateurs de succès pour « {base} »",
            f"🤖 Identifier les modules IA ou compétences nécessaires à « {base} »",
            f"🧠 Réfléchir à l’impact cognitif de « {base} » sur l’agent",
            f"🧬 Analyser la faisabilité technique ou logique de « {base} »"
        ]
        return random.sample(modèles, k=3)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif_raw = ctx.get("objectif", "")
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", "")).strip()
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw.strip()
        else:
            objectif = str(objectif_raw).strip()

        if not objectif:
            plugins_log.append("StrategieObjectifsPlugin : 🚫 Aucun objectif à décomposer.")
            logger.info("[strategie_objectifs] Aucun objectif fourni.")
            return ctx

        sous_objectifs = self.generer_sous_objectifs(objectif)

        if sous_objectifs:
            ctx["objectifs_secondaires"] = sous_objectifs
            plugins_log.append(f"StrategieObjectifsPlugin : 🎯 Sous-objectifs générés → {len(sous_objectifs)}")
            logger.info(f"[strategie_objectifs] Sous-objectifs générés pour « {objectif} » : {sous_objectifs}")
        else:
            plugins_log.append("StrategieObjectifsPlugin : ❌ Échec de la génération.")
            logger.warning("[strategie_objectifs] Aucun sous-objectif généré.")

        return ctx
