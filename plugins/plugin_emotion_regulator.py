from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.emotion_regulator")

class PluginEmotionRegulator(BasePlugin):
    meta = Meta(
        name="plugin_emotion_regulator",
        version="1.0",
        priority=2.8,  # Juste avant l’appel LLM
        author="Toi & GPT"
    )

    EMOTION_STYLES = {
        "joy": "Réponds avec une touche chaleureuse, positive et encourageante.",
        "sadness": "Réponds avec douceur, compassion et compréhension.",
        "anger": "Réponds avec calme, patience et une volonté de résoudre les tensions.",
        "neutral": "Réponds de manière professionnelle et factuelle.",
        "confused": "Réponds avec clarté, pédagogie et rassurance.",
        "enthusiastic": "Réponds avec énergie, curiosité et encouragement."
    }

    def detect_emotion(self, message: str) -> str:
        """Détection simplifiée d’émotions à partir du message utilisateur."""
        message = message.lower()
        if any(w in message for w in ["je suis content", "heureux", "cool", "génial"]):
            return "joy"
        elif any(w in message for w in ["triste", "déçu", "fatigué", "mal"]):
            return "sadness"
        elif any(w in message for w in ["énervé", "rage", "fâché", "marre"]):
            return "anger"
        elif any(w in message for w in ["?", "comprends pas", "c'est flou", "bizarre"]):
            return "confused"
        elif any(w in message for w in ["trop bien", "super", "incroyable", "hype"]):
            return "enthusiastic"
        else:
            return "neutral"

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        if not message.strip():
            ctx.setdefault("plugins_log", []).append("plugin_emotion_regulator : message vide.")
            return ctx

        emotion = self.detect_emotion(message)
        style_instruction = self.EMOTION_STYLES.get(emotion, self.EMOTION_STYLES["neutral"])

        existing_style = ctx.get("style_instruction", "")
        ctx["style_instruction"] = f"{existing_style.strip()} {style_instruction}".strip()

        logger.info(f"[emotion_regulator] Emotion détectée : {emotion} → ton adapté.")
        ctx.setdefault("plugins_log", []).append(
            f"plugin_emotion_regulator : style enrichi pour émotion '{emotion}'"
        )

        return ctx
