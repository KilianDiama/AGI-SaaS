# plugins/plugin_autogen_structurel.py

"""
Plugin : autogen_structurel
Rôle   : Génère des suggestions de modification de l’architecture cognitive (plugins, priorités, stratégies)
Priorité : 101 (après noyau_conscient, avant rendu final)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autogen_structurel")

class AutogenStructurelPlugin(BasePlugin):
    meta = Meta(
        name="autogen_structurel",
        priority=101,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        plugins_logiques = ctx.get("emergence_logique", [])
        objections = ctx.get("contre_arguments", [])
        memoires = ctx.get("memoires_emergentes", [])
        score = ctx.get("score_cognitif", 70)

        propositions = []

        if len(objections) >= 3:
            propositions.append("🛠 Désactiver temporairement le plugin logique dominant pour réduire la rigidité.")
        if score < 60:
            propositions.append("📉 Réorganiser les priorités pour renforcer la synthèse avant la simulation.")
        if len(memoires) > 10:
            propositions.append("🧹 Purger ou condenser la mémoire émergente pour réduire surcharge cognitive.")
        if not plugins_logiques:
            propositions.append("➕ Ajouter un module d’émergence logique plus fin (ex. analogie).")

        if not propositions:
            propositions.append("✅ Aucun ajustement requis : architecture stable.")

        ctx["auto_modifications_proposees"] = propositions
        log.append(f"AutogenStructurelPlugin : {len(propositions)} suggestion(s) de reconfiguration.")
        logger.info(f"[autogen_structurel] Propositions : {propositions}")

        return ctx
