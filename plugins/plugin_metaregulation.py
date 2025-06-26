"""
Plugin : metaregulation
Rôle : Surveiller les autres plugins et détecter comportements anormaux ou inefficaces
Priorité : 7 (dernière étape du cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.metaregulation")

class MetaRegulationPlugin(BasePlugin):
    meta = Meta(
        name="metaregulation",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.get("plugins_log", [])
        rapport = []
        alertes = []

        if not plugins_log:
            ctx["metaregulation"] = "❌ Aucun plugin à analyser."
            return ctx

        # Analyse simple : détection de motifs excessifs ou suspects
        repetitions = {}
        for log in plugins_log:
            base = log.split(":")[0].strip()
            repetitions[base] = repetitions.get(base, 0) + 1

        for plugin, count in repetitions.items():
            if count > 2:
                msg = f"🔁 Plugin {plugin} exécuté {count} fois — possible boucle."
                rapport.append(msg)
                alertes.append(plugin)

        if any("contradiction" in p.lower() for p in plugins_log):
            rapport.append("⚠️ Contradiction logique détectée, nécessite validation logique renforcée.")

        if ctx.get("objectif", {}).get("but") not in ctx.get("llm_response", ""):
            rapport.append("🎯 Réponse non directement liée à l’objectif — possible dérive.")

        ctx["metaregulation"] = "\n".join(rapport) if rapport else "✅ Aucune dérive détectée"
        ctx["plugins_a_surveiller"] = alertes
        plugins_log.append("MetaRegulationPlugin : analyse des dynamiques cognitives")
        logger.info(f"[metaregulation] Surveillance terminée, alertes : {alertes}")

        return ctx
