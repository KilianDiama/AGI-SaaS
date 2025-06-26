# plugins/plugin_structure_verificateur.py

"""
Plugin : plugin_structure_verificateur
Rôle : Vérifie la qualité de la structure de la réponse (lisibilité, clarté, format)
Priorité : 4.1 (juste avant raffinement final)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.structure_verificateur")

class PluginStructureVerificateur(BasePlugin):
    meta = Meta(
        name="plugin_structure_verificateur",
        priority=4.1,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        réponse = ctx.get("llm_response", "") or ctx.get("response", "")
        if not réponse.strip():
            ctx.setdefault("plugins_log", []).append("plugin_structure_verificateur : aucune réponse à vérifier")
            return ctx

        feedbacks = []

        # Vérifie la présence de paragraphes
        if réponse.count("\n") < 2:
            feedbacks.append("🔻 La réponse manque de paragraphes — structure plate.")

        # Vérifie la ponctuation de fin
        if not re.search(r"[.!?…]$", réponse.strip()):
            feedbacks.append("⚠️ La réponse ne se termine pas correctement (pas de ponctuation).")

        # Vérifie la longueur minimale
        if len(réponse.strip()) < 50:
            feedbacks.append("📏 Réponse très courte — manque de développement.")

        # Vérifie si markdown ou style est présent
        if "**" not in réponse and "-" not in réponse:
            feedbacks.append("🎨 Style peu structuré (absence de mise en forme).")

        if feedbacks:
            ctx["structure_feedback"] = "\n".join(feedbacks)
            ctx.setdefault("plugins_log", []).append("plugin_structure_verificateur : structure perfectible")
            logger.info(f"[structure] Feedback :\n{ctx['structure_feedback']}")
        else:
            ctx.setdefault("plugins_log", []).append("plugin_structure_verificateur : structure OK")

        return ctx
