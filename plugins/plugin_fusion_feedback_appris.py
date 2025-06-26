import logging
import os
import json
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.fusion_feedback_appris")

class FusionFeedbackApprisPlugin(BasePlugin):
    meta = Meta(
        name="fusion_feedback_appris",
        priority=2.9,
        version="1.1",  # bump de version
        author="AGI & Matthieu"
    )

    FEEDBACK_PATH = "feedback_historique.json"

    def charger_feedbacks(self):
        if os.path.exists(self.FEEDBACK_PATH):
            try:
                with open(self.FEEDBACK_PATH, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
                    else:
                        logger.warning("[fusion_feedback_appris] Fichier vide, initialisation liste vide.")
            except Exception as e:
                logger.error(f"[fusion_feedback_appris] Erreur lecture JSON : {e}")
        return []

    def enregistrer_feedback(self, feedbacks):
        try:
            with open(self.FEEDBACK_PATH, "w", encoding="utf-8") as f:
                json.dump(feedbacks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"[fusion_feedback_appris] Erreur sauvegarde JSON : {e}")

    async def run(self, ctx: Context) -> Context:
        try:
            plugins_log = ctx.setdefault("plugins_log", [])
            feedback_actuel = ctx.get("feedback_utilisateur", "").strip().lower()
            message = ctx.get("message", "")
            feedbacks = self.charger_feedbacks()

            if feedback_actuel in ["oui", "bien", "parfait", "👍"]:
                feedbacks.append({"message": message, "eval": "positif"})
            elif feedback_actuel in ["non", "nul", "mauvais", "👎"]:
                feedbacks.append({"message": message, "eval": "negatif"})

            # Ne garder que les 50 derniers
            if len(feedbacks) > 50:
                feedbacks = feedbacks[-50:]

            self.enregistrer_feedback(feedbacks)
            plugins_log.append("FusionFeedbackApprisPlugin : feedback intégré")
            logger.info("[fusion_feedback_appris] Feedback utilisateur enregistré.")

            # Influence légère sur le contexte
            positif = sum(1 for f in feedbacks if f.get("eval") == "positif")
            negatif = sum(1 for f in feedbacks if f.get("eval") == "negatif")

            tonalite = ctx.get("tonalite_utilisateur", "neutre")
            if positif > negatif and tonalite == "neutre":
                ctx["tonalite_utilisateur"] = "positif"

        except Exception as e:
            logger.exception("[fusion_feedback_appris] Erreur dans run()")
            ctx.setdefault("errors", []).append({
                "plugin": self.meta.name,
                "error": str(e)
            })

        return ctx
