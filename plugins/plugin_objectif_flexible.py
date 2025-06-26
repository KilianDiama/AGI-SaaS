# plugins/plugin_objectif_flexible.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_flexible")

class PluginObjectifFlexible(BasePlugin):
    meta = Meta(
        name="plugin_objectif_flexible",
        version="1.0",
        priority=1.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        if isinstance(message, dict):
            message = message.get("content", "")
        message = str(message).strip().lower()

        now = datetime.utcnow().isoformat()
        log = ctx.setdefault("plugins_log", [])
        anciens = ctx.get("historique_objectifs", [])

        if not message:
            objectif = "clarifier l’intention de l’utilisateur à partir d’un message vide ou ambigu"
            note = 6.0
            justification = "Message vide — objectif de clarification activé."
        else:
            # Dictionnaires de détection
            categories = {
                "finance": {
                    "mots": ["riche", "million", "millionnaire", "argent", "revenu", "fortune", "investir", "passif"],
                    "objectif": "élaborer une stratégie d’enrichissement durable et adaptée",
                    "note": 9.3,
                    "raison": "Objectif financier détecté"
                },
                "quêtedesens": {
                    "mots": ["sens", "vie", "but", "mission", "direction"],
                    "objectif": "explorer les valeurs personnelles et la mission de vie",
                    "note": 9.0,
                    "raison": "Recherche existentielle perçue"
                },
                "organisation": {
                    "mots": ["plan", "étapes", "organiser", "structurer", "objectif", "projet"],
                    "objectif": "mettre en place un plan structuré et cohérent",
                    "note": 8.8,
                    "raison": "Demande organisationnelle"
                },
                "emotion": {
                    "mots": ["seul", "fatigué", "déprimé", "angoissé", "perdu", "triste"],
                    "objectif": "fournir un soutien émotionnel adapté et bienveillant",
                    "note": 8.5,
                    "raison": "État émotionnel détecté"
                }
            }

            objectif, note, justification = None, 7.0, "Aucun signal fort — réponse utile générique."
            for cat in categories.values():
                if any(m in message for m in cat["mots"]):
                    objectif = cat["objectif"]
                    note = cat["note"]
                    justification = cat["raison"]
                    break

            if not objectif:
                objectif = f"répondre utilement à la demande : « {message} »"

        if objectif in anciens:
            note -= 1.0
            justification += " (objectif déjà rencontré)."

        ctx["objectif_generé"] = {
            "objectif": objectif,
            "note": round(note, 2),
            "commentaire": justification,
            "timestamp": now
        }

        ctx["objectif_general"] = objectif
        log.append(f"PluginObjectifFlexible : objectif → {objectif} (note {round(note, 2)})")
        logger.info(f"[objectif_flexible] Objectif généré : {objectif} | Note : {round(note, 2)}")

        return ctx
