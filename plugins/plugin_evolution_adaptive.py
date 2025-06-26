""" 
Plugin : evolution_adaptive  
Rôle : Proposer des modifications internes selon l’analyse cognitive du système  
Priorité : 9.0 (dernier plugin logique avant fin de cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.evolution_adaptive")

class EvolutionAdaptivePlugin(BasePlugin):
    meta = Meta(
        name="evolution_adaptive",
        priority=9.0,
        version="1.0",
        author="Matthieu & GPT"
    )

    def analyser_contexte(self, ctx: Context) -> str:
        vital = ctx.get("signal_vital", "")
        contestation = ctx.get("auto_contestation", "")
        metacog = ctx.get("metacognition", "")
        suggestions = []

        if "🔴" in vital:
            suggestions.append("↯ Réduire la charge cognitive en abaissant le nombre de plugins actifs par cycle.")
        if "⚠️" in contestation or "erreur" in contestation.lower():
            suggestions.append("⚙️ Renforcer les modules d’autocontrôle et de test logique.")
        if "trop de redondance" in metacog.lower():
            suggestions.append("🌀 Optimiser la synthèse pour éviter la répétition des réponses.")

        if not suggestions:
            suggestions.append("✅ Aucun changement nécessaire — système stable pour ce cycle.")

        return "\n".join(suggestions)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        proposition = self.analyser_contexte(ctx)

        ctx["mutation_proposee"] = f"🧬 Proposition d’évolution interne :\n{proposition}"

        if not ctx.get("response"):
            ctx["response"] = ctx["mutation_proposee"]

        plugins_log.append("EvolutionAdaptivePlugin : suggestion d’évolution produite.")
        logger.info("[evolution_adaptive] Proposition de mutation injectée.")

        return ctx
