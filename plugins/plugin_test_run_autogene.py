"""
Plugin : test_run_autogene
Rôle : Déclencher et enchaîner automatiquement tous les plugins d’auto-évolution AGI
Priorité : 1.0 (exécution immédiate en début de cycle)
Auteur : Matthieu & GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.test_run_autogene")

class TestRunAutogenePlugin(BasePlugin):
    meta = Meta(
        name="test_run_autogene",
        priority=1.0,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Simuler un déclenchement manuel
        ctx["declenche_autoevolution"] = True
        plugins_log.append("TestRunAutogenePlugin : démarrage du cycle d'auto-évolution.")

        # Ordre de déclenchement implicite (les autres plugins seront appelés naturellement)
        ctx["message"] = (
            "Commencer un cycle complet d'auto-amélioration. "
            "Analyse → idée → code → évaluation → déploiement → journalisation."
        )

        logger.info("[test_run_autogene] Cycle d’évolution déclenché.")
        return ctx
