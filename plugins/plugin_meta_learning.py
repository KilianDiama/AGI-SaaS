# plugins/plugin_meta_learning.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.meta_learning")

class PluginMetaLearning(BasePlugin):
    meta = Meta(
        name="plugin_meta_learning",
        priority=5.5,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        evaluation = ctx.get("evaluation", {})
        historique = ctx.get("historique", [])
        ajustements = []

        note = evaluation.get("note", 0)
        longueur = evaluation.get("longueur", 0)
        alignement = evaluation.get("alignement_intention", 0)

        # Heuristiques adaptatives
        if note < 2:
            ajustements.append("⚠️ Réponses à simplifier (note faible)")
        if longueur > 1000:
            ajustements.append("✂️ Trop long — réduire la taille des sorties")
        if alignement < 0.5:
            ajustements.append("🎯 Améliorer l’alignement avec l’intention")

        # Mise à jour du contexte
        ctx["meta_learning"] = {
            "ajustements_proposés": ajustements,
            "derniere_note": note,
            "commentaire": "📊 Ajustements proposés selon l’évaluation récente.",
            "alignement": alignement
        }

        ctx.setdefault("plugins_log", []).append(f"PluginMetaLearning : {len(ajustements)} ajustement(s) suggéré(s)")
        logger.info(f"[meta_learning] Ajustements recommandés : {ajustements}")

        return ctx
