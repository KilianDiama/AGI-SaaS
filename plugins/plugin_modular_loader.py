# plugins/plugin_modular_loader.py

"""
Plugin : plugin_modular_loader
Rôle : Injecter dynamiquement une composition de plugins à exécuter
Priorité : 2.9 (juste après plugin_flexible_composer)
Auteur : Matt & GPT
"""

import logging
from typing import List
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.modular_loader")

class PluginModularLoader(BasePlugin):
    meta = Meta(
        name="plugin_modular_loader",
        version="1.0",
        priority=2.9,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        composition: List[str] = ctx.get("composition_dynamique", [])

        if not composition:
            logger.info("[plugin_modular_loader] Aucune composition dynamique définie.")
            ctx.setdefault("plugins_log", []).append("plugin_modular_loader : aucune composition dynamique")
            return ctx

        # Injection dans le contexte pour forcer l'exécution de certains plugins
        ctx["plugins_forcés"] = composition
        logger.info(f"[plugin_modular_loader] Plugins injectés dynamiquement : {composition}")
        ctx.setdefault("plugins_log", []).append(
            f"plugin_modular_loader : plugins injectés {composition}"
        )

        return ctx
