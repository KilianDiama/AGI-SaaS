# plugins/plugin_orchestrateur_personnalise.py

import importlib
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.orchestrateur_personnalise")

class PluginOrchestrateurPersonnalise(BasePlugin):
    meta = Meta(
        name="plugin_orchestrateur_personnalise",
        version="1.0",
        priority=4.0,  # après le filtre
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins = ctx.get("pipeline_plugins_filtrés", [])

        for plugin_name in plugins:
            try:
                module_path = f"plugins.{plugin_name}"
                module = importlib.import_module(module_path)
                plugin_class = getattr(module, plugin_name_to_class(plugin_name))
                plugin_instance = plugin_class()

                if hasattr(plugin_instance, "run"):
                    ctx = await plugin_instance.run(ctx)
                    logger.info(f"[{plugin_name}] exécuté avec succès.")
                    ctx.setdefault("plugins_log", []).append(f"{plugin_name} exécuté.")
                else:
                    logger.warning(f"[{plugin_name}] n’a pas de méthode `run()`.")

            except Exception as e:
                logger.error(f"[{plugin_name}] échec d’exécution : {e}")
                ctx.setdefault("plugins_log", []).append(f"{plugin_name} erreur : {e}")

        return ctx

def plugin_name_to_class(plugin_name):
    # ex: plugin_test_logger → PluginTestLogger
    return ''.join([part.capitalize() for part in plugin_name.split('_')])
