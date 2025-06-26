"""
Plugin : evenements_marquants
Rôle : Identifier et mémoriser les événements cognitifs significatifs dans les cycles
Priorité : 6 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.evenements_marquants")

class EvenementsMarquantsPlugin(BasePlugin):
    meta = Meta(
        name="evenements_marquants",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        marqueurs = ctx.setdefault("evenements_marquants", [])
        trace = []

        # Signaux d'événements marquants
        if "⚠️ Contradictions détectées" in ctx.get("validation_logique", ""):
            trace.append("🧨 Contradiction interne identifiée.")

        if "réponse très longue" in ctx.get("auto_debug", "").lower():
            trace.append("🗯️ Verbosité excessive détectée.")

        if "changement de but" in ctx.get("objectif_log", ""):
            trace.append("🎯 Objectif modifié en cours de raisonnement.")

        if ctx.get("memoire_transversale") and "lien détecté" in ctx["memoire_transversale"]:
            trace.append("🔗 Connexions mnésiques significatives.")

        if "création spontanée" in ctx.get("creativite_libre", "").lower():
            trace.append("🎨 Moment d’expression créative notable.")

        if trace:
            moment = {
                "cycle": len(ctx.get("historique_evolution", [])),
                "timestamp": ctx.get("timestamp", "inconnu"),
                "faits": trace,
                "contexte_resume": ctx.get("llm_response", "")[:200]
            }
            marqueurs.append(moment)
            plugins_log.append(f"EvenementsMarquantsPlugin : {len(trace)} événement(s) enregistré(s)")
            logger.info("[evenements_marquants] Marqueurs détectés")

        else:
            plugins_log.append("EvenementsMarquantsPlugin : rien de significatif")
            logger.info("[evenements_marquants] Pas d’événement remarquable")

        return ctx
