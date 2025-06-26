# plugins/plugin_auto_adjusteur_pipeline.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.auto_adjusteur")

class PluginAutoAdjusteurPipeline(BasePlugin):
    meta = Meta(
        name="plugin_auto_adjusteur_pipeline",
        version="1.0",
        priority=9.5,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        mémoire_plugins = ctx.get("memoire_plugins", {})
        pipeline = ctx.get("pipeline", [])

        pipeline_ajusté = []
        for plugin in pipeline:
            stats = mémoire_plugins.get(plugin, None)
            if stats:
                total = stats["ok"] + stats["fail"]
                taux_echec = stats["fail"] / total if total > 0 else 0

                # Si le plugin a échoué plus de 50% du temps, on le désactive temporairement
                if taux_echec > 0.5:
                    logger.warning(f"⚠️ Plugin {plugin} désactivé (taux d’échec: {taux_echec:.0%})")
                    ctx.setdefault("plugins_log", []).append(f"{self.meta.name} : {plugin} désactivé (taux échec)")
                    continue

            pipeline_ajusté.append(plugin)

        ctx["pipeline"] = pipeline_ajusté
        ctx.setdefault("plugins_log", []).append(f"{self.meta.name} : pipeline ajusté dynamiquement.")
        return ctx
