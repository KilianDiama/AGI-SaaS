# plugins/plugin_superviseur_global.py

"""
Plugin : superviseur_global
Rôle   : Orchestration intelligente — ajuste dynamiquement les plugins actifs selon le contexte, la performance ou les objectifs
Priorité : -50 (exécuté tôt, juste après init_cycle)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.superviseur_global")

class SuperviseurGlobalPlugin(BasePlugin):
    meta = Meta(
        name="superviseur_global",
        priority=-50,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif_general", "générer une réponse")
        score_precedent = ctx.get("dernier_score", 80)
        reflexion_globale = ctx.get("reflexion_globale", "")
        demande = ctx.get("demande_llm", "").lower()

        plugins_à_désactiver = []
        plugins_à_renforcer = []

        # Exemple 1 : si tendance négative ou score bas → activer auto_diagnostic
        if reflexion_globale == "baisse d'efficacité cognitive" or score_precedent < 60:
            plugins_à_renforcer += ["self_diagnostic", "meta_regulation", "reflexion_transversale"]
            log.append("SuperviseurGlobalPlugin : régulation renforcée (efficacité ↓)")

        # Exemple 2 : si l'utilisateur demande une explication ou du raisonnement profond
        if "pourquoi" in demande or "analyse" in demande:
            plugins_à_renforcer += ["raisonneur", "reflexion", "meta_reasoner"]

        # Exemple 3 : si la mission est technique ou critique → activer cohérence & logique
        if any(mot in objectif for mot in ["audit", "vérification", "plan"]):
            plugins_à_renforcer += ["verificateur_logique", "planificateur_competent"]

        # Exemple 4 : si trop de surcharge ou contexte court → alléger le pipeline
        if len(ctx.get("messages", [])) > 10:
            plugins_à_désactiver += ["mutation_cognitive", "evolution_guidée"]
            log.append("SuperviseurGlobalPlugin : réduction charge cognitive")

        # Appliquer dans le contexte
        ctx["plugins_a_renforcer"] = list(set(plugins_à_renforcer))
        ctx["plugins_a_desactiver"] = list(set(plugins_à_désactiver))
        log.append("SuperviseurGlobalPlugin : ajustements suggérés appliqués")
        logger.info(f"[superviseur_global] Plugins renforcés : {plugins_à_renforcer}")
        logger.info(f"[superviseur_global] Plugins désactivés : {plugins_à_désactiver}")

        return ctx
