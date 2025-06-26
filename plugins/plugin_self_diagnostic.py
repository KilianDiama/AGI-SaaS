# plugins/plugin_self_diagnostic.py

"""
Plugin : self_diagnostic
Rôle   : Auto-évaluation du cycle cognitif — détecte les échecs, incohérences, ou anomalies de raisonnement
Priorité : 5 (doit être exécuté après le raisonnement mais avant la synthèse finale)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.self_diagnostic")

class SelfDiagnosticPlugin(BasePlugin):
    meta = Meta(
        name="self_diagnostic",
        priority=5,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.get("plugins_log", [])
        response = ctx.get("llm_response", "")
        diagnostics = []

        # ⚠️ Vérifie si la réponse LLM est vide
        if not response.strip():
            diagnostics.append("Aucune réponse produite par les modules LLM.")

        # ❗ Détecte des formulations faibles ou non informatives
        if response.lower() in ["je ne sais pas", "aucune idée", "désolé"]:
            diagnostics.append("Réponse incertaine ou non informative détectée.")

        # 🔍 Scanne les logs pour erreurs ou avertissements explicites
        for line in logs:
            if "erreur" in line.lower() or "échec" in line.lower():
                diagnostics.append(f"⚠️ Log critique : {line}")

        # 🧠 Cherche des contradictions avec les hypothèses
        hypotheses = ctx.get("hypotheses", [])
        for hypo in hypotheses:
            if hypo.lower() in response.lower():
                diagnostics.append(f"Contradiction possible avec l'hypothèse : « {hypo} »")

        # ➕ Insère les diagnostics dans le contexte
        if diagnostics:
            ctx["diagnostic_auto"] = diagnostics
            ctx.setdefault("plugins_log", []).append(f"SelfDiagnosticPlugin : {len(diagnostics)} anomalies détectées.")
            logger.warning(f"[self_diagnostic] Anomalies détectées : {diagnostics}")
        else:
            ctx.setdefault("plugins_log", []).append("SelfDiagnosticPlugin : aucun problème détecté.")
            logger.info("[self_diagnostic] Aucun problème détecté.")

        return ctx
