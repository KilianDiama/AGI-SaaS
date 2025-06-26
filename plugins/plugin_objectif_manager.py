# plugins/plugin_objectif_manager.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.objectif_manager")

class PluginObjectifManager(BasePlugin):
    meta = Meta(
        name="plugin_objectif_manager",
        version="1.0",
        priority=0.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        objectif = {
            "but": "non défini",
            "état": "à faire",
            "priorité": 1
        }

        if not message:
            objectif["but"] = "aucun message utilisateur détecté"
        elif "résume" in message or "résumé" in message:
            objectif["but"] = "générer un résumé de contenu"
        elif "analyse" in message or "analyse-moi" in message:
            objectif["but"] = "analyser un texte ou un contexte"
        elif "code" in message or "programme" in message:
            objectif["but"] = "générer ou analyser du code"
        elif "idée" in message or "projet" in message:
            objectif["but"] = "brainstorming d’idée ou plan de projet"
        else:
            objectif["but"] = "répondre à une question générale"

        ctx["objectif"] = objectif
        ctx.setdefault("plugins_log", []).append(f"PluginObjectifManager : objectif détecté → {objectif['but']}")
        logger.info(f"[objectif] Objectif déterminé : {objectif}")

        return ctx
