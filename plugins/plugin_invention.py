""" 
Plugin : invention  
Rôle : Générer une invention ou idée originale basée sur la mémoire, l'objectif et la réflexion interne  
Priorité : 5.5 (juste après fusion, avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.invention")

class InventionPlugin(BasePlugin):
    meta = Meta(
        name="invention",
        priority=5.5,
        version="1.1",  # ← version corrigée
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self):
        if os.path.exists(self.MEMOIRE_PATH):
            try:
                with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except Exception as e:
                logger.warning(f"[invention] Erreur lecture mémoire : {e}")
        return []

    def normaliser_objectif(self, obj):
        if isinstance(obj, dict):
            return str(obj.get("but", "")).strip()
        return str(obj).strip()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif_raw = ctx.get("objectif", "")
        objectif = self.normaliser_objectif(objectif_raw)

        base_reflexion = ctx.get("reflexion_interne", "")
        memoire = self.charger_memoire()
        inspiration = "une expérience passée"

        if memoire and isinstance(memoire, list):
            item = random.choice(memoire)
            if isinstance(item, dict):
                inspiration = item.get("objectif", inspiration)

        invention = (
            f"À partir de {inspiration}, je propose une idée originale :\n"
            f"💡 Invention : Un module qui s'auto-évalue en temps réel pendant l'élaboration de sa réponse.\n"
            f"Cela permettrait à l'IA de détecter des contradictions ou manques de clarté avant même de finaliser sa réponse."
        )

        ctx["idee_inventee"] = invention
        if not ctx.get("response"):
            ctx["response"] = invention

        plugins_log.append("InventionPlugin : idée/invention générée.")
        logger.info(f"[invention] Idée inventée : {invention[:80]}...")

        return ctx
