# plugins/plugin_consistance_contextuelle.py

"""
Plugin : plugin_consistance_contextuelle
Rôle : Vérifier et améliorer la cohérence entre les messages passés et la réponse actuelle
Priorité : 2.3 (après mémoire et raisonnement, avant génération finale)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.consistance_contextuelle")

class PluginConsistanceContextuelle(BasePlugin):
    meta = Meta(
        name="plugin_consistance_contextuelle",
        priority=2.3,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        réponse = ctx.get("llm_response", "")
        feedbacks = []

        if not historique or not réponse:
            ctx.setdefault("plugins_log", []).append("plugin_consistance_contextuelle : données insuffisantes")
            return ctx

        # Analyse simple de rupture de sujet
        dernier_msg = historique[-1].get("message", "").strip().lower()
        if dernier_msg and len(dernier_msg) > 15 and dernier_msg[:7] != réponse[:7].lower():
            feedbacks.append("🔁 La réponse semble déconnectée du dernier message.")

        # Vérifie la cohérence avec le résumé mémoire
        résumé = ctx.get("memoire_contextuelle", "")
        if résumé and résumé not in réponse:
            feedbacks.append("📌 Le résumé contextuel n'est pas réutilisé dans la réponse.")

        if feedbacks:
            ctx["consistance_feedback"] = "\n".join(feedbacks)
            ctx.setdefault("plugins_log", []).append("plugin_consistance_contextuelle : cohérence partielle")
            logger.info(f"[consistance] Feedback :\n{ctx['consistance_feedback']}")
        else:
            ctx.setdefault("plugins_log", []).append("plugin_consistance_contextuelle : OK")

        return ctx
