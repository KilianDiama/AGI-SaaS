# plugins/plugin_profiling_perf.py

"""
Plugin : plugin_profiling_perf
Rôle : Mesurer le temps d'exécution et l'utilisation mémoire de chaque plugin pour l'optimisation de la performance
Priorité : 0.1 (très tôt dans le cycle pour activer les hooks globaux)
Auteur : Matt & GPT
"""

import logging
import time
import tracemalloc
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.profiling_perf")

class PluginProfilingPerf(BasePlugin):
    meta = Meta(
        name="plugin_profiling_perf",
        version="1.0",
        priority=0.1,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logger.info("[profiling_perf] Activation des hooks de profiling performance.")

        # Activer le tracemalloc
        tracemalloc.start()

        # Injecte les hooks dans le contexte global (ou dans un gestionnaire partagé)
        def _plugin_start(name):
            start = time.perf_counter()
            ctx.setdefault("_profiling", {})[name] = {
                "start": start,
                "memory_start": tracemalloc.get_traced_memory()[1]
            }
            return start

        def _plugin_end(start, name):
            end = time.perf_counter()
            mem_current, mem_peak = tracemalloc.get_traced_memory()
            stats = ctx.get("_profiling", {}).get(name, {})
            duration = end - stats.get("start", start)
            mem_used = mem_peak - stats.get("memory_start", 0)
            
            logger.info(f"[profiling_perf] ⏱ Plugin {name} → {duration:.3f}s, 📦 mémoire +{mem_used/1024:.1f} Ko")
            ctx.setdefault("plugins_log", []).append(
                f"profiling_perf : {name} → {duration:.3f}s, +{mem_used/1024:.1f} Ko"
            )

        # Injecter dans le contexte pour accès global par le moteur
        ctx["_plugin_start"] = _plugin_start
        ctx["_plugin_end"] = _plugin_end

        return ctx
