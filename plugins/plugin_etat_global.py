# plugins/plugin_etat_global.py

"""
Plugin : etat_global
Rôle   : Évalue l’état cognitif global du système : surcharge, conflits, efficacité, clarté
Priorité : 104 (ultime plugin du cycle)
Auteur  : Toi + GPT
"""

import logging
from statistics import mean
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.etat_global")

class EtatGlobalPlugin(BasePlugin):
    meta = Meta(
        name="etat_global",
        priority=104,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        score = ctx.get("score_cognitif", 0)
        objections = ctx.get("contre_arguments", [])
        concepts = ctx.get("emergence_logique", [])
        reflexion = ctx.get("reflexion_globale", "")
        diagnostics = ctx.get("diagnostic_auto", [])
        plugins = ctx.get("ordre_plugins", [])

        # Calculs heuristiques
        surcharge = len(plugins) > 15
        instabilité = len(diagnostics) > 2
        contradiction = len(objections) > 2

        # Note de stabilité
        stabilite = 100
        if surcharge: stabilite -= 10
        if instabilité: stabilite -= 15
        if contradiction: stabilite -= 10
        if score < 60: stabilite -= 15

        stabilite = max(0, min(100, stabilite))

        # Synthèse
        rapport = {
            "stabilite_cognitive": stabilite,
            "surcharge_detectee": surcharge,
            "instabilite_detectee": instabilité,
            "niveau_reflexif": reflexion or "non évalué",
            "objections_integrées": len(objections),
            "structures_logiques_detectées": len(concepts),
            "plugins_utilisés": len(plugins),
        }

        ctx["etat_global"] = rapport
        log.append(f"EtatGlobalPlugin : état global évalué → stabilité = {stabilite}")
        logger.info(f"[etat_global] Rapport global : {rapport}")

        return ctx
