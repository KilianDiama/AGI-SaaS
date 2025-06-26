# plugins/plugin_objectif_generator.py

import re
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_generator")

class PluginObjectifGenerator(BasePlugin):
    meta = Meta(
        name="plugin_objectif_generator",
        priority=1.0,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        memoire = ctx.get("memoire_profonde", {})
        objectifs = []

        if not message or not isinstance(message, str):
            ctx["objectifs_detectés"] = []
            ctx.setdefault("plugins_log", []).append("PluginObjectifGenerator : message vide ou invalide ❌")
            return ctx

        objectifs = self._extraire_objectifs(message)

        ctx["objectifs_detectés"] = objectifs
        ctx.setdefault("plugins_log", []).append(
            f"PluginObjectifGenerator : {len(objectifs)} objectif(s) détecté(s) ✅"
        )
        logger.info(f"[objectif_generator] Objectifs extraits : {objectifs}")
        return ctx

    def _extraire_objectifs(self, message: str) -> list:
        objectifs = []

        # Analyse textuelle simple
        if re.search(r"\b(créer|développer|faire)\b", message, re.IGNORECASE):
            objectifs.append("produire un résultat concret")

        if re.search(r"\b(améliorer|optimiser)\b", message, re.IGNORECASE):
            objectifs.append("améliorer un processus ou une réponse")

        if re.search(r"\b(analyser|étudier|comprendre)\b", message, re.IGNORECASE):
            objectifs.append("extraire une compréhension")

        if re.search(r"\b(planifier|structurer)\b", message, re.IGNORECASE):
            objectifs.append("organiser les étapes d’un plan d’action")

        # Objectif de secours
        if not objectifs:
            objectifs.append("clarifier la demande utilisateur")

        return objectifs
