# plugins/plugin_meta_feedback.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.meta_feedback")

class PluginMetaFeedback(BasePlugin):
    meta = Meta(
        name="plugin_meta_feedback",
        version="1.0",
        priority=6.8,  # Après la réponse générée mais avant export/sauvegarde
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse = ctx.get("llm_response", "").strip()
        intention = ctx.get("intention", "").strip()
        objectif = ctx.get("objectif", {}).get("but", "").strip()
        style = ctx.get("style_instruction", "")
        feedbacks = []

        if not reponse:
            feedbacks.append("❌ Aucune réponse générée.")

        if "?" in reponse and not intention:
            feedbacks.append("🤔 Réponse interrogative alors que l’intention n’est pas claire.")

        if objectif.lower() in ("", "répondre à une question générale"):
            feedbacks.append("📌 Objectif trop flou, affinement nécessaire.")

        if "**" not in reponse and "clair" in style:
            feedbacks.append("📉 Style possiblement pas conforme aux instructions de clarté/structuration.")

        if len(reponse.split()) < 10:
            feedbacks.append("🪶 Réponse trop brève pour être utile.")

        commentaire = "\n".join(feedbacks) or "✅ Cycle globalement satisfaisant."
        ctx["meta_feedback"] = commentaire

        ctx.setdefault("plugins_log", []).append("PluginMetaFeedback : feedback métacognitif injecté.")
        logger.info(f"[meta_feedback] Auto-évaluation du cycle :\n{commentaire}")

        return ctx
