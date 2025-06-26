import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memory_importer")

class PluginMemoryImporter(BasePlugin):
    meta = Meta(
        name="plugin_memory_importer",
        version="1.0",
        priority=0.9,  # Avant analyse, réflexion, raisonnement
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("memoire_long_terme", {}).get("historique", [])
        résumé = ctx.get("memoire_long_terme", {}).get("résumé", "")
        derniers_objectifs = ctx.get("memoire_long_terme", {}).get("objectifs", [])

        contenus = []

        if résumé:
            contenus.append(f"🧠 Résumé passé :\n{résumé}")
        if derniers_objectifs:
            contenus.append(f"🎯 Objectifs précédents :\n- " + "\n- ".join(derniers_objectifs))
        if historique:
            extraits = "\n".join(h["message"] for h in historique[-3:])
            contenus.append(f"💬 Derniers messages :\n{extraits}")

        if contenus:
            mémoire = "\n\n".join(contenus)
            ctx["memoire_contextuelle"] = mémoire
            ctx.setdefault("plugins_log", []).append("PluginMemoryImporter : mémoire injectée")
            logger.info("[memory_importer] Mémoire contextuelle restaurée.")
        else:
            logger.info("[memory_importer] Aucune mémoire à restaurer.")

        return ctx
