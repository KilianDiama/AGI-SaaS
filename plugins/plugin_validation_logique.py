"""
Plugin : validation_logique
Rôle : Vérifier la cohérence logique élémentaire des assertions générées
Priorité : 5 (après génération de réponse)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.validation_logique")

class ValidationLogiquePlugin(BasePlugin):
    meta = Meta(
        name="validation_logique",
        priority=5,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        assertions = ctx.get("llm_response", "")

        if not assertions.strip():
            ctx["validation_logique"] = "❌ Aucune assertion à vérifier."
            plugins_log.append("ValidationLogiquePlugin : rien à valider")
            return ctx

        contradictions = []

        lignes = assertions.lower().split("\n")
        for line in lignes:
            if "je suis certain que" in line and "je ne suis pas sûr que" in line:
                contradictions.append(line)
            if "tout" in line and "rien" in line:
                contradictions.append(line)
            if "impossible" in line and "peut-être" in line:
                contradictions.append(line)

        if contradictions:
            message = "⚠️ Contradictions détectées dans le raisonnement :\n\n"
            for c in contradictions:
                message += f"• {c.strip()}\n"
            ctx["validation_logique"] = message
            plugins_log.append("ValidationLogiquePlugin : contradictions repérées")
            logger.warning("[validation_logique] Contradictions repérées")
        else:
            ctx["validation_logique"] = "✅ Aucun paradoxe logique évident détecté."
            plugins_log.append("ValidationLogiquePlugin : raisonnement cohérent")
            logger.info("[validation_logique] Raisonnement validé")

        return ctx
