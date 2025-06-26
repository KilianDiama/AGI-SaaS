import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectif_long_terme")

class PluginObjectifLongTerme(BasePlugin):
    meta = Meta(
        name="plugin_objectif_long_terme",
        version="1.0",
        priority=1.2,  # Après contexte, avant analyse
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectifs = ctx.setdefault("objectifs_long_terme", [])
        current_obj = ctx.get("objectif", {}).get("but", "").strip().lower()

        # Vérifie si un objectif long-terme doit être intégré
        if current_obj and current_obj not in [o.lower() for o in objectifs]:
            objectifs.append(current_obj)
            logger.info(f"[ObjectifLongTerme] Nouvel objectif enregistré : {current_obj}")

        # Injection si aucun objectif défini
        if not current_obj and objectifs:
            ctx["objectif"] = {
                "but": objectifs[-1],
                "état": "en cours",
                "priorité": 1
            }
            logger.info(f"[ObjectifLongTerme] Objectif réinjecté : {objectifs[-1]}")
            ctx.setdefault("plugins_log", []).append("PluginObjectifLongTerme : objectif long-terme restauré")

        # Nettoyage périodique (évite suraccumulation)
        if len(objectifs) > 10:
            objectifs[:] = objectifs[-10:]
            logger.info("[ObjectifLongTerme] Liste des objectifs réduite à 10 derniers")

        return ctx
