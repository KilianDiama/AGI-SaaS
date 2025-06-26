from noyau_core import BasePlugin, Context, Meta
import logging
import json

logger = logging.getLogger("plugin.cycle_reviewer")

class PluginCycleReviewer(BasePlugin):
    meta = Meta(
        name="plugin_cycle_reviewer",
        version="1.0",
        priority=5.0,  # À exécuter après tout le reste, pour review complète
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        try:
            plugins = ctx.get("plugins_log", [])
            response = ctx.get("llm_response", ctx.get("llm_response_votée", ""))
            objectif = ctx.get("objectif", {}).get("but", "inconnu")
            intention = ctx.get("intention", "inconnue")
            erreurs = ctx.get("errors", [])
            reflex = ctx.get("reflexion_interne", "")
            analyse = ctx.get("analysis_feedback", "")
            plan = ctx.get("plan", [])
            temps = ctx.get("ts_start", "?") + " → " + ctx.get("ts_end", "?")

            lignes = [
                "🧩 **Cycle LLM Review**",
                f"📌 Objectif : {objectif}",
                f"🎯 Intention détectée : {intention}",
                f"🕓 Durée : {temps}",
                "",
                "🛠️ **Plugins exécutés** :",
                "\n".join(f"• {log}" for log in plugins[-10:]),
                "",
                "⚠️ **Erreurs détectées** :" if erreurs else "✅ Aucune erreur détectée.",
            ]

            if erreurs:
                lignes += [f"- {err['plugin']} : {err['error']}" for err in erreurs]

            if reflex:
                lignes += ["", "🧠 Réflexion interne :", reflex]

            if analyse:
                lignes += ["", "🔎 Analyse :", analyse]

            if plan:
                lignes += ["", "🧭 Plan suivi :"]
                lignes += [f"• {step['étape']} ({step['status']})" for step in plan]

            lignes += ["", "📤 **Réponse finale** :", response[:500] + ("..." if len(response) > 500 else "")]

            ctx["cycle_review_summary"] = "\n".join(lignes)
            ctx.setdefault("plugins_log", []).append("PluginCycleReviewer : synthèse du cycle générée.")
            logger.info("[cycle_reviewer] Synthèse du cycle créée.")
        except Exception as e:
            logger.warning(f"[cycle_reviewer] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append(f"PluginCycleReviewer : erreur → {e}")

        return ctx
