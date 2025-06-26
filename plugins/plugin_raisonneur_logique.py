# plugins/plugin_raisonneur_logique.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.raisonneur_logique")

class PluginRaisonneurLogique(BasePlugin):
    meta = Meta(
        name="plugin_raisonneur_logique",
        version="1.0",
        priority=98.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("demande_llm") or ctx.get("llm_prompt", "")
        if not message:
            ctx.setdefault("plugins_log", []).append("PluginRaisonneurLogique : aucun message à raisonner.")
            return ctx

        raisonnement = (
            "🔍 Raisonnement logique :\n"
            "- Identifier les éléments clés du message\n"
            "- Analyser la relation entre ces éléments\n"
            "- Déduire les actions ou réponses logiques possibles\n"
            "- Choisir la réponse la plus cohérente avec l’objectif"
        )

        ctx["llm_prompt"] = (
            f"{message.strip()}\n\n"
            f"{raisonnement}\n"
            "🧠 Réponds maintenant en expliquant brièvement ta démarche avant de conclure."
        )
        ctx.setdefault("plugins_log", []).append("PluginRaisonneurLogique : raisonnement injecté.")
        return ctx
