# plugins/plugin_memoire_objectifs_longs.py

import json
import os
import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_objectifs_longs")

class PluginMemoireObjectifsLongs(BasePlugin):
    meta = Meta(
        name="plugin_memoire_objectifs_longs",
        priority=2.9,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.fichier = "data/memoire_objectifs.json"
        os.makedirs(os.path.dirname(self.fichier), exist_ok=True)
        if not os.path.exists(self.fichier):
            with open(self.fichier, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    async def run(self, ctx: Context) -> Context:
        action = ctx.get("memoire_action", "")
        contenu = ctx.get("objectif_texte", "")
        etat_filtre = ctx.get("etat_filtre", None)

        if action == "ajouter" and contenu:
            result = self.ajouter_objectif(contenu)
            ctx["memoire_objectifs_longs_result"] = result
            logger.info(f"[Mémoire Objectifs] Objectif ajouté → {contenu}")

        elif action == "filtrer":
            result = self.filtrer_objectifs(etat_filtre)
            ctx["memoire_objectifs_longs_result"] = result
            logger.info(f"[Mémoire Objectifs] Objectifs filtrés → {etat_filtre or 'tous'}")

        else:
            ctx.setdefault("plugins_log", []).append("PluginMemoireObjectifsLongs : action invalide ou données manquantes")
            logger.warning("[Mémoire Objectifs] Aucune action valide détectée")

        return ctx

    def charger(self) -> list:
        try:
            with open(self.fichier, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erreur chargement mémoire : {e}")
            return []

    def sauvegarder(self, data: list) -> None:
        try:
            with open(self.fichier, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde mémoire : {e}")

    def ajouter_objectif(self, texte: str, priorite: int = 1) -> dict:
        objectifs = self.charger()
        now = datetime.utcnow().isoformat()
        nouveau = {
            "objectif": texte,
            "priorite": priorite,
            "etat": "en attente",
            "timestamp": now
        }
        objectifs.append(nouveau)
        self.sauvegarder(objectifs)
        return nouveau

    def filtrer_objectifs(self, etat: str = None) -> list:
        objectifs = self.charger()
        if etat:
            return [o for o in objectifs if o.get("etat") == etat]
        return objectifs
