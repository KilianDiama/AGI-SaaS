# plugins/plugin_conscience_iterative.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.conscience_iterative")

class PluginConscienceIterative(BasePlugin):
    meta = Meta(
        name="plugin_conscience_iterative",
        version="1.0",
        priority=98.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        last_response = ctx.get("llm_response", "").strip()
        plan = ctx.get("plan", [])
        reflexions = ctx.get("reflexions_creatives", [])

        conscience = {
            "réponse_vide": last_response == "",
            "réponse_trop_courte": len(last_response) < 30,
            "réponse_confuse": any(word in last_response.lower() for word in ["je ne sais pas", "désolé", "aucune idée"]),
            "étapes_incomplètes": any(etape.get("status") != "terminé" for etape in plan),
            "besoin_reformulation": False
        }

        # Auto-évaluation
        verdicts = []
        if conscience["réponse_vide"]:
            verdicts.append("⚠️ Réponse absente.")
        if conscience["réponse_trop_courte"]:
            verdicts.append("🟡 Réponse brève.")
        if conscience["réponse_confuse"]:
            verdicts.append("🔴 Réponse confuse ou incomplète.")
        if conscience["étapes_incomplètes"]:
            verdicts.append("⏳ Plan non terminé.")
        if reflexions:
            verdicts.append("✅ Créativité utilisée.")

        bilan = "\n".join(verdicts) or "✅ Rien à signaler. Cycle cohérent."

        ctx["conscience_iterative"] = {
            "analyse": conscience,
            "bilan": bilan
        }

        ctx.setdefault("plugins_log", []).append("PluginConscienceIterative : auto-évaluation du cycle.")
        return ctx
