# plugins/plugin_executant_proactif.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.executant_proactif")

class PluginExecutantProactif(BasePlugin):
    meta = Meta(
        name="plugin_executant_proactif",
        version="1.0",
        author="Toi & GPT",
        priority=3.5
    )

    def __init__(self):
        self.nom = "plugin_executant_proactif"

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan_long_terme", {}).get("plan", [])
        if not plan:
            logger.info(f"[{self.nom}] Aucun plan détecté.")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun plan à exécuter.")
            return ctx

        objectifs_a_faire = [obj for obj in plan if obj["status"] == "à faire"]
        if not objectifs_a_faire:
            logger.info(f"[{self.nom}] Aucun objectif à exécuter.")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : tous les objectifs sont traités.")
            return ctx

        objectif = objectifs_a_faire[0]
        action = self._traduire_objectif_en_action(objectif["objectif"])

        if action:
            ctx.setdefault("tâches_proactives", []).append(action)
            objectif["status"] = "en cours"
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : action déclenchée → {action}")
        else:
            logger.warning(f"[{self.nom}] Aucun plugin assigné à : {objectif['objectif']}")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun plugin trouvé pour {objectif['objectif']}")

        return ctx

    def _traduire_objectif_en_action(self, objectif: str) -> str:
        objectif = objectif.lower()
        if "répondre" in objectif:
            return "activer_plugin_raisonneur"
        if "analyser" in objectif:
            return "activer_plugin_analyse_semantique"
        if "structurer" in objectif:
            return "activer_plugin_planificateur"
        if "créer" in objectif:
            return "activer_plugin_creatif"
        return ""
