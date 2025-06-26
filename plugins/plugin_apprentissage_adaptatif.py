# plugins/plugin_apprentissage_adaptatif.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.apprentissage_adaptatif")

class PluginApprentissageAdaptatif(BasePlugin):
    meta = Meta(
        name="plugin_apprentissage_adaptatif",
        version="1.0",
        author="Toi & GPT",
        priority=3.0
    )

    def __init__(self):
        self.nom = "plugin_apprentissage_adaptatif"

    async def run(self, ctx: Context) -> Context:
        historique_plugins = ctx.get("plugins_log", [])
        auto_eval = ctx.get("self_eval_score", {})
        note = auto_eval.get("note", 0)
        verdict = auto_eval.get("verdict", "inconnu")

        seuil_bon_score = 7.0

        if note >= seuil_bon_score:
            strategie = {
                "config": ctx.get("llm_config", {}),
                "plugins": ctx.get("composition_dynamique", []),
                "note": note,
                "verdict": verdict,
                "mode": ctx.get("mode_strategique", "inconnu")
            }
            ctx.setdefault("memoire_strategies", []).append(strategie)
            logger.info(f"[{self.nom}] ✅ Stratégie mémorisée (note = {note})")
        else:
            erreur = {
                "plugins": historique_plugins[-5:],
                "note": note,
                "verdict": verdict
            }
            ctx.setdefault("erreurs_recentes", []).append(erreur)
            logger.info(f"[{self.nom}] ⚠️ Analyse d'échec (note = {note})")

        ctx.setdefault("plugins_log", []).append(f"{self.nom} : apprentissage basé sur score = {note}")
        return ctx
