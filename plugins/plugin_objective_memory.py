from noyau_core import BasePlugin, Context, Meta
import logging
import datetime

logger = logging.getLogger("plugin.objective_memory")

class PluginObjectiveMemory(BasePlugin):
    meta = Meta(
        name="plugin_objective_memory",
        version="1.0",
        priority=2.5,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but")
        historique = ctx.setdefault("objectifs_mémorisés", [])

        if objectif and objectif.lower() not in ["", "répondre à une question générale"]:
            # Éviter les doublons trop fréquents
            if objectif not in [o["but"] for o in historique]:
                historique.append({
                    "but": objectif,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                logger.info(f"[objective_memory] Objectif mémorisé : {objectif}")
                ctx.setdefault("plugins_log", []).append(f"PluginObjectiveMemory : objectif ajouté → {objectif}")
        else:
            logger.debug("[objective_memory] Aucun objectif spécifique à mémoriser.")

        ctx["objectifs_mémorisés"] = historique
        return ctx
