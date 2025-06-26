# plugins/plugin_self_strategy_planner.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.self_strategy_planner")


class PluginSelfStrategyPlanner(BasePlugin):
    meta = Meta(
        name="plugin_self_strategy_planner",
        priority=1.9,  # après objectif, avant raisonnement
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "")
        historique = ctx.get("history", [])
        contexte_utilisateur = ctx.get("user_config", {})

        resultat = self.generer_plan_strategique(objectif, historique, contexte_utilisateur)

        ctx["plan_strategique_auto"] = resultat
        ctx.setdefault("plugins_log", []).append(f"PluginSelfStrategyPlanner : {resultat['etat']}")
        logger.info(f"[SelfStrategy] Plan généré → {resultat['etat']}")
        return ctx

    def generer_plan_strategique(self, objectif: str, historique: list, contexte_utilisateur: dict) -> dict:
        plan = []
        ts = datetime.utcnow().isoformat()

        if not objectif:
            return {
                "etat": "inactif",
                "raison": "Aucun objectif détecté.",
                "timestamp": ts
            }

        objectif = objectif.lower()

        plan.append("🔍 Analyse du besoin utilisateur")
        if "apprendre" in objectif or "comprendre" in objectif:
            plan.extend([
                "📚 Fournir une explication claire et progressive",
                "🧪 Ajouter un exemple concret"
            ])
        if "corriger" in objectif or "erreur" in objectif:
            plan.extend([
                "🛠️ Identifier l'erreur ou incohérence",
                "✅ Proposer une correction claire"
            ])
        if "améliorer" in objectif or "optimiser" in objectif:
            plan.extend([
                "📈 Évaluer les performances actuelles",
                "🧩 Proposer des pistes d’amélioration concrètes"
            ])
        if "générer" in objectif:
            plan.extend([
                "🧠 Proposer une structure de génération",
                "🎯 Affiner le style et le ton attendus"
            ])

        plan.extend([
            "🧠 Auto-évaluation de la cohérence",
            "♻️ Régénération si le score de qualité est faible",
            "🔄 Adapter tonalité et style à l’évolution du ton utilisateur"
        ])

        return {
            "etat": "actif",
            "timestamp": ts,
            "objectif": objectif,
            "contexte": contexte_utilisateur,
            "plan_strategique": plan
        }
