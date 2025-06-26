# plugins/plugin_gestion_objectifs.py

import json
import os
import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.gestion_objectifs")

OBJECTIFS_FILE = "data/objectifs_persistants.json"

class GestionObjectifsPlugin(BasePlugin):
    meta = Meta(
        name="plugin_gestion_objectifs",
        version="1.3",  # version mise à jour
        priority=1.2,
        author="Toi & GPT"
    )

    def __init__(self):
        super().__init__()
        self.objectifs = self._charger_objectifs()

    def _charger_objectifs(self):
        if os.path.exists(OBJECTIFS_FILE):
            try:
                with open(OBJECTIFS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
                    else:
                        logger.error("[Objectifs] Format invalide : attendu un dictionnaire.")
            except Exception as e:
                logger.error(f"[Objectifs] Erreur lecture : {e}")
        return {}

    def _sauver_objectifs(self):
        try:
            os.makedirs(os.path.dirname(OBJECTIFS_FILE), exist_ok=True)
            with open(OBJECTIFS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.objectifs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[Objectifs] Erreur sauvegarde : {e}")

    def ajouter_objectif(self, objectif: str, priorité: int = 1) -> str:
        id_obj = f"obj-{len(self.objectifs)+1}-{int(datetime.utcnow().timestamp())}"
        self.objectifs[id_obj] = {
            "objectif": objectif,
            "état": "à faire",
            "priorité": priorité,
            "timestamp": datetime.utcnow().isoformat(),
            "sous_objectifs": []
        }
        self._sauver_objectifs()
        return id_obj

    def marquer_comme_fait(self, id_obj: str):
        if id_obj in self.objectifs:
            self.objectifs[id_obj]["état"] = "terminé"
            self._sauver_objectifs()

    def générer_plan(self, objectif: str):
        return [
            f"Analyser l’objectif « {objectif} »",
            "Identifier contraintes et dépendances",
            "Décomposer en étapes claires",
            "Proposer solution ou stratégie",
            "Implémenter et vérifier"
        ]

    def injecter_sous_objectifs(self, id_obj: str):
        if id_obj in self.objectifs:
            obj = self.objectifs[id_obj]
            if isinstance(obj, dict) and not obj.get("sous_objectifs"):
                plan = self.générer_plan(obj.get("objectif", "objectif inconnu"))
                obj["sous_objectifs"] = [{"tâche": step, "état": "à faire"} for step in plan]
                self._sauver_objectifs()

    def obtenir_prochain_objectif(self):
        objectifs_triés = sorted(
            self.objectifs.items(),
            key=lambda item: (item[1].get("état") != "terminé", item[1].get("priorité", 1))
        )
        for obj_id, data in objectifs_triés:
            if data.get("état") in ("à faire", "en cours"):
                return obj_id, data
        return None, None

    def état_global(self) -> dict:
        return {
            "total": len(self.objectifs),
            "en cours": sum(1 for o in self.objectifs.values() if o.get("état") == "en cours"),
            "à faire": sum(1 for o in self.objectifs.values() if o.get("état") == "à faire"),
            "terminé": sum(1 for o in self.objectifs.values() if o.get("état") == "terminé")
        }

    async def run(self, ctx: Context) -> Context:
        try:
            plugins_log = ctx.setdefault("plugins_log", [])
            id_obj, data = self.obtenir_prochain_objectif()

            if id_obj and isinstance(data, dict):
                objectif = data.get("objectif", "inconnu")
                ctx["objectif"] = data
                ctx["objectif_id"] = id_obj
                plugins_log.append(f"GestionObjectifsPlugin : objectif courant → {objectif}")
                logger.info(f"[plugin.gestion_objectifs] Objectif actif → {objectif}")
            else:
                plugins_log.append("GestionObjectifsPlugin : aucun objectif actif.")
                logger.info("[plugin.gestion_objectifs] Aucun objectif actif trouvé.")

        except Exception as e:
            logger.exception("[plugin_gestion_objectifs] Erreur dans run()")
            ctx.setdefault("errors", []).append({
                "plugin": self.meta.name,
                "error": str(e)
            })

        return ctx
