""" 
Plugin : emotion_simulee  
Rôle : Simuler une réaction émotionnelle symbolique en fonction du raisonnement et de l’objectif  
Priorité : 6.9 (après dialectique, avant création de réponse finale)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.emotion_simulee")

class EmotionSimuleePlugin(BasePlugin):
    meta = Meta(
        name="emotion_simulee",
        priority=6.9,
        version="1.1",  # mise à jour version
        author="Matthieu & GPT"
    )

    def evaluer_contexte(self, objectif: str, signal: str) -> str:
        objectif = str(objectif).lower()
        signal = str(signal).lower()

        if "erreur" in signal or "échec" in objectif:
            return "😟 Frustration simulée : un obstacle inattendu a été perçu."
        elif "nouveau" in objectif or "créatif" in objectif:
            return "🤩 Enthousiasme simulé : l’idée stimule une exploration positive."
        elif "danger" in objectif or "risque" in signal:
            return "⚠️ Inquiétude simulée : prudence activée face à une incertitude."
        else:
            return random.choice([
                "🙂 Sérénité cognitive simulée.",
                "😐 Neutralité analytique active.",
                "🤔 Intérêt curieux généré artificiellement."
            ])

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = ctx.get("objectif", "")
        signal = ctx.get("signal_vital", "")

        if not objectif:
            plugins_log.append("EmotionSimuleePlugin : rien à évaluer émotionnellement.")
            return ctx

        emotion = self.evaluer_contexte(objectif, signal)
        ctx["emotion_simulee"] = emotion

        if not ctx.get("response"):
            ctx["response"] = f"{emotion}\n\n{ctx.get('response', '')}"

        plugins_log.append("EmotionSimuleePlugin : réaction émotionnelle artificielle ajoutée.")
        logger.info(f"[emotion_simulee] Emotion générée : {emotion}")

        return ctx
