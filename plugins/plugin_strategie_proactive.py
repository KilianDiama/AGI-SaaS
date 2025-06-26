from noyau_core import BasePlugin, Context, Meta
import logging
import datetime

logger = logging.getLogger("plugin.strategie_proactive")

class PluginStrategieProactive(BasePlugin):
    meta = Meta(
        name="plugin_strategie_proactive",
        version="1.0",
        priority=1.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("memoire_contextuelle", "")
        now = datetime.datetime.now().isoformat()
        objectifs = []

        # 🔎 Analyse des sujets fréquents ou abandonnés
        if "data" in historique.lower():
            objectifs.append("Analyser la qualité des données récemment reçues.")

        if "plugin" in historique.lower():
            objectifs.append("Auditer la cohérence et la couverture des plugins.")

        if "erreur" in historique.lower():
            objectifs.append("Identifier les patterns d’erreurs récurrentes et proposer des solutions.")

        # 🎯 Déclencheur d’objectif périodique
        if now.endswith("T12:00:00"):  # À midi
            objectifs.append("Effectuer un auto-check de performance quotidienne.")

        # 🧠 Si aucun objectif explicite : proposer une exploration
        if not ctx.get("objectif", {}).get("but"):
            objectifs.append("Explorer les connaissances internes et proposer des optimisations.")

        if objectifs:
            ctx["objectif_propose"] = {
                "timestamp": now,
                "propositions": objectifs
            }
            ctx.setdefault("plugins_log", []).append("PluginStrategieProactive : propositions d’objectifs générées.")
            logger.info(f"[stratégie proactive] Objectifs suggérés : {objectifs}")

        return ctx
