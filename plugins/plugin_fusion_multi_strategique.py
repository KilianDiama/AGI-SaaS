from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.fusion_multi_strategique")

class PluginFusionMultiStrategique(BasePlugin):
    meta = Meta(
        name="plugin_fusion_multi_strategique",
        version="1.0",
        priority=4.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        blocs = []

        reflexion = ctx.get("reflexion_interne", "")
        if reflexion:
            blocs.append(f"🤔 **Réflexion** :\n{reflexion.strip()}")

        raisonnement = ctx.get("response_logique") or ctx.get("raisonneur_response", "")
        if raisonnement:
            blocs.append(f"🧠 **Raisonnement** :\n{raisonnement.strip()}")

        resume = ctx.get("llm_summary") or ctx.get("auto_summary", "")
        if resume:
            blocs.append(f"📄 **Résumé** :\n{resume.strip()}")

        feedback = ctx.get("analysis_feedback", "")
        if feedback:
            blocs.append(f"📊 **Feedback** :\n{feedback.strip()}")

        sémantique = ctx.get("poids_semantique", {})
        if sémantique:
            score = sémantique.get("score", 0)
            mots = ", ".join(sémantique.get("mots_cles", []))
            blocs.append(f"🧪 **Analyse sémantique** : score {score:.2f}, mots clés : {mots}")

        if blocs:
            ctx["response"] = "\n\n".join(blocs)
            ctx.setdefault("plugins_log", []).append("PluginFusionMultiStrategique : réponse enrichie combinée")
        else:
            ctx["response"] = "Aucune information stratégique disponible à fusionner."
            ctx.setdefault("plugins_log", []).append("PluginFusionMultiStrategique : aucun bloc disponible")

        return ctx
