import logging
import os
import json
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_conceptuelle")

class MemoireConceptuellePlugin(BasePlugin):
    meta = Meta(
        name="memoire_conceptuelle",
        priority=1.6,
        version="1.2",  # version corrigée
        author="AGI & Matthieu"
    )

    CONCEPTS_PATH = "memoire_conceptuelle.json"

    def charger_concepts(self):
        if os.path.exists(self.CONCEPTS_PATH):
            try:
                with open(self.CONCEPTS_PATH, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
                    else:
                        logger.warning("[memoire_conceptuelle] Fichier vide, initialisation d'un nouveau dictionnaire.")
            except Exception as e:
                logger.error(f"[memoire_conceptuelle] Erreur lecture JSON : {e}")
        return {}

    def sauvegarder_concepts(self, concepts):
        try:
            with open(self.CONCEPTS_PATH, "w", encoding="utf-8") as f:
                json.dump(concepts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[memoire_conceptuelle] Erreur sauvegarde : {e}")

    async def run(self, ctx: Context) -> Context:
        try:
            plugins_log = ctx.setdefault("plugins_log", [])
            message_raw = ctx.get("message", "")
            if not isinstance(message_raw, str):
                plugins_log.append("MemoireConceptuellePlugin : message invalide (non string)")
                return ctx

            message = message_raw.lower()
            concepts = self.charger_concepts()
            lexique = {
                "autonomie": "capacité à agir sans intervention",
                "empathie": "adapter le ton au ressenti de l’utilisateur",
                "raisonnement": "enchaînement logique de décisions",
                "créativité": "générer des idées inédites ou inattendues"
            }

            concepts_detectes = []

            for mot_cle, definition in lexique.items():
                if mot_cle in message:
                    if mot_cle not in concepts:
                        concepts[mot_cle] = []
                    if definition not in concepts[mot_cle]:
                        concepts[mot_cle].append(definition)
                        concepts_detectes.append(mot_cle)

            if concepts_detectes:
                self.sauvegarder_concepts(concepts)
                ctx["concepts_memorises"] = concepts_detectes
                logger.info(f"[memoire_conceptuelle] Concepts mémorisés : {concepts_detectes}")
                plugins_log.append(f"MemoireConceptuellePlugin : concepts mémorisés → {concepts_detectes}")
            else:
                plugins_log.append("MemoireConceptuellePlugin : aucun concept détecté.")

        except Exception as e:
            logger.exception("[memoire_conceptuelle] Erreur dans run()")
            ctx.setdefault("errors", []).append({
                "plugin": self.meta.name,
                "error": str(e)
            })

        return ctx
