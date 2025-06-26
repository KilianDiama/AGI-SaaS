# plugins/plugin_memoire_evaluative.py

import logging
from noyau_core import BasePlugin, Context, Meta
from datetime import datetime

logger = logging.getLogger("plugin.memoire_evaluative")

class PluginMemoireEvaluative(BasePlugin):
    meta = Meta(
        name="plugin_memoire_evaluative",
        version="1.0",
        priority=9.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.get("plugins_log", [])
        mémoire = ctx.setdefault("memoire_plugins", {})

        for log_entry in logs:
            if "exécuté" in log_entry or "erreur" in log_entry:
                plugin_name = log_entry.split(":")[0].strip()
                statut = "ok" if "exécuté" in log_entry else "fail"
                mémoire.setdefault(plugin_name, {
                    "ok": 0,
                    "fail": 0,
                    "last_seen": None
                })

                mémoire[plugin_name][statut] += 1
                mémoire[plugin_name]["last_seen"] = datetime.utcnow().isoformat()

        ctx["memoire_plugins"] = mémoire
        logger.info(f"📥 Mémoire évaluative mise à jour.")
        ctx.setdefault("plugins_log", []).append("plugin_memoire_evaluative : mémoire enregistrée.")
        return ctx
