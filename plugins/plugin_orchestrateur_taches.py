# plugins/plugin_orchestrateur_taches.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.orchestrateur_taches")

class PluginOrchestrateurTaches(BasePlugin):
    meta = Meta(
        name="plugin_orchestrateur_taches",
        version="1.0",
        author="Toi & GPT",
        priority=4.0
    )

    def __init__(self):
        self.nom = "plugin_orchestrateur_taches"

    async def run(self, ctx: Context) -> Context:
        taches = ctx.get("tâches_proactives", [])

        if not taches:
            logger.info(f"[{self.nom}] Aucune tâche proactive à exécuter.")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucune tâche à exécuter.")
            return ctx

        for tache in taches:
            plugin_name = self._extraire_plugin(tache)
            if plugin_name:
                success = await self._executer_plugin(plugin_name, ctx)
                if success:
                    ctx.setdefault("plugins_log", []).append(f"{self.nom} : tâche exécutée → {plugin_name}")
                else:
                    ctx.setdefault("plugins_log", []).append(f"{self.nom} : échec tâche → {plugin_name}")
            else:
                logger.warning(f"[{self.nom}] Tâche mal formée : {tache}")
                ctx.setdefault("plugins_log", []).append(f"{self.nom} : tâche invalide → {tache}")

        ctx["tâches_proactives"] = []
        return ctx

    def _extraire_plugin(self, action: str) -> str:
        if action.startswith("activer_plugin_"):
            return action.replace("activer_", "").strip()
        return ""

    async def _executer_plugin(self, plugin_name: str, ctx: Context) -> bool:
        registre = ctx.get("plugins_register", {})
        plugin = registre.get(plugin_name)
        if not plugin:
            logger.warning(f"[{self.nom}] Plugin '{plugin_name}' introuvable dans le registre.")
            return False

        if hasattr(plugin, "run") and callable(plugin.run):
            try:
                result = await plugin.run(ctx)
                if result:
                    ctx.update(result)
                return True
            except Exception as e:
                logger.error(f"[{self.nom}] Erreur lors de l’exécution de '{plugin_name}': {e}")
                return False
        elif hasattr(plugin, "tick") and callable(plugin.tick):
            try:
                plugin.tick(ctx)
                return True
            except Exception as e:
                logger.error(f"[{self.nom}] Erreur dans tick() de '{plugin_name}': {e}")
                return False
        else:
            logger.warning(f"[{self.nom}] Plugin '{plugin_name}' ne contient ni run() ni tick().")
            return False
