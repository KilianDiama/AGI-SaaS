# plugins/plugin_lien_intercycle.py

from noyau_core import BasePlugin, Context, Meta
import logging
import os
import json

logger = logging.getLogger("plugin.lien_intercycle")

class PluginLienInterCycle(BasePlugin):
    meta = Meta(
        name="plugin_lien_intercycle",
        version="1.0",
        priority=0.8,  # Très tôt dans le cycle
        author="Toi & GPT"
    )

    HISTORY_PATH = "/mnt/data/context_archive"

    def _charger_contexte_precedent(self):
        fichiers = sorted(
            [f for f in os.listdir(self.HISTORY_PATH) if f.endswith(".json")],
            reverse=True
        )
        if not fichiers:
            return None
        dernier = fichiers[0]
        with open(os.path.join(self.HISTORY_PATH, dernier), "r", encoding="utf-8") as f:
            return json.load(f)

    async def run(self, ctx: Context) -> Context:
        if not os.path.exists(self.HISTORY_PATH):
            os.makedirs(self.HISTORY_PATH)

        precedent = self._charger_contexte_precedent()
        if precedent:
            resume = precedent.get("memoire_contextuelle", "")
            objectif = precedent.get("objectif", {}).get("but", "")
            if resume:
                ctx["memoire_lien"] = resume
                ctx.setdefault("plugins_log", []).append("PluginLienInterCycle : mémoire précédente injectée.")
                logger.info(f"[intercycle] Résumé mémoire précédente injecté.")
            if objectif:
                ctx["objectif_precedent"] = objectif

        return ctx
