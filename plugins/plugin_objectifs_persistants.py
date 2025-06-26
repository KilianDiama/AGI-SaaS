import os
import json
from datetime import datetime
from typing import Dict, List

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.objectifs_persistants")

FICHIER_OBJECTIFS = "data/objectifs_persistants.json"

class PluginObjectifsPersistants(BasePlugin):
    meta = Meta(
        name="plugin_objectifs_persistants",
        version="1.0",
        priority=1.3,
        author="Toi & GPT"
    )

    def _charger_objectifs(self) -> Dict[str, List[Dict]]:
        if os.path.exists(FICHIER_OBJECTIFS):
            with open(FICHIER_OBJECTIFS, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _sauvegarder_objectifs(self, data: Dict[str, List[Dict]]):
        os.makedirs(os.path.dirname(FICHIER_OBJECTIFS), exist_ok=True)
        with open(FICHIER_OBJECTIFS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    async def run(self, ctx: Context) -> Context:
        user_id = ctx.get("user", {}).get("id") or "anonymous"
        objectifs_data = self._charger_objectifs()

        # Charger les anciens objectifs s'il y en a
        anciens = objectifs_data.get(user_id, [])
        if anciens:
            ctx["objectifs_persistants"] = anciens
            logger.info(f"[objectifs_persistants] Objectifs retrouvés pour {user_id} ({len(anciens)})")
        else:
            ctx["objectifs_persistants"] = []

        # Ajouter un nouvel objectif si détecté
        nouvel_objectif = ctx.get("objectif", {})
        if nouvel_objectif and nouvel_objectif.get("but"):
            nouvel_objectif["timestamp"] = datetime.utcnow().isoformat()
            if not any(o["but"] == nouvel_objectif["but"] for o in anciens):
                anciens.append(nouvel_objectif)
                objectifs_data[user_id] = anciens
                self._sauvegarder_objectifs(objectifs_data)
                logger.info(f"[objectifs_persistants] Objectif sauvegardé pour {user_id}")

        ctx.setdefault("plugins_log", []).append("PluginObjectifsPersistants : objectifs persistants gérés.")
        return ctx
