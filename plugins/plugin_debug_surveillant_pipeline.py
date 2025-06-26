# plugins/plugin_debug_surveillant_pipeline.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.debug_surveillant")

class PluginDebugSurveillantPipeline(BasePlugin):
    meta = Meta(
        name="plugin_debug_surveillant_pipeline",
        version="1.0",
        priority=9.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        pipeline = ctx.get("pipeline", [])
        plugins_log = ctx.setdefault("plugins_log", [])

        logger.info("📊 Supervision pipeline actuelle :")
        plugins_log.append(f"{self.meta.name} : supervision du pipeline :")

        for i, plugin in enumerate(pipeline):
            msg = f"🔢 {i+1}. {plugin}"
            logger.info(msg)
            plugins_log.append(msg)

        plugins_log.append(f"{self.meta.name} : pipeline total → {len(pipeline)} plugins.")
        return ctx
