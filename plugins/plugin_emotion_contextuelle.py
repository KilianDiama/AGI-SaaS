"""
Plugin : emotion_contextuelle
Rôle : Adapter la réponse à l'émotion perçue dans la question utilisateur
Priorité : 12
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.emotion_contextuelle")

class EmotionContextuellePlugin(BasePlugin):
    meta = Meta(
        name="emotion_contextuelle",
        priority=12,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    tons = {
        "détresse": ["je ne comprends pas", "aide-moi", "je suis perdu", "ça ne marche pas"],
        "colère": ["c’est nul", "pourquoi ça bug", "fais ce que je dis", "ça m’énerve"],
        "joie": ["trop bien", "merci", "j’adore", "super", "trop cool"],
        "curiosité": ["comment", "pourquoi", "peux-tu", "explique-moi", "montre-moi"]
    }

    réponses_types = {
        "détresse": "🫂 Je suis là. On va résoudre ça ensemble, étape par étape.",
        "colère": "😌 D’accord, restons calmes. Dis-moi précisément ce que tu veux corriger.",
        "joie": "🥰 Merci beaucoup ! Ça me fait plaisir de t’aider.",
        "curiosité": "🔍 Allons explorer ça ensemble. Voilà ce que je peux t’expliquer..."
    }

    def détecter_ton(self, message: str) -> str:
        message = message.lower()
        for ton, mots in self.tons.items():
            if any(re.search(rf"\b{re.escape(m)}\b", message) for m in mots):
                return ton
        return "curiosité"

    async def run(self, ctx: Context) -> Context:
        msg = ctx.get("message", "")
        plugins_log = ctx.setdefault("plugins_log", [])

        ton = self.détecter_ton(msg)
        réponse_type = self.réponses_types.get(ton)

        ctx.setdefault("préambules_emotionnels", []).append({
            "ton_detecté": ton,
            "message_origine": msg,
            "ajouté": réponse_type
        })

        ctx["llm_pre_prompt"] = réponse_type + "\n\n" + ctx.get("llm_pre_prompt", "")
        plugins_log.append(f"EmotionContextuellePlugin : ton détecté = {ton}")
        logger.info(f"[emotion_contextuelle] Ton identifié : {ton}")

        return ctx
