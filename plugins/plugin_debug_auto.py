import time
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.debug_auto")

class PluginDebugAuto(BasePlugin):
    meta = Meta(
        name="plugin_debug_auto",
        version="1.0",
        priority=9.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        try:
            start = time.perf_counter()

            summary = {
                "cycle_id": ctx.get("cycle_id"),
                "user": ctx.get("user", {}).get("email", "inconnu"),
                "intention": ctx.get("intention"),
                "étape": ctx.get("tache_courante"),
                "objectif": ctx.get("objectif", {}).get("but"),
                "plugins_invoqués": ctx.get("plugins_log", []),
                "erreurs": ctx.get("errors", []),
            }

            duration = time.perf_counter() - start
            summary["temps_debug"] = f"{duration:.4f}s"

            ctx["debug_auto_summary"] = summary
            ctx.setdefault("plugins_log", []).append("PluginDebugAuto : debug résumé injecté.")
            logger.debug(f"[debug_auto] Résumé exécution : {summary}")

        except Exception as e:
            logger.warning(f"[debug_auto] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append(f"PluginDebugAuto : erreur → {e}")

        return ctx
