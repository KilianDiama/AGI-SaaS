"""
Plugin : dialogue_facettes
Rôle : Faire dialoguer plusieurs voix internes (rêveuse, critique, sage, etc.)
Priorité : 26
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.dialogue_facettes")

class DialogueFacettesPlugin(BasePlugin):
    meta = Meta(
        name="dialogue_facettes",
        priority=26,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    profils = {
        "sage": {
            "intro": "Posons les fondations, calmement.",
            "style": "structuré et réfléchi"
        },
        "rêveuse": {
            "intro": "Je vois les choses autrement, dans un monde qui ondule.",
            "style": "métaphorique, sensoriel"
        },
        "critique": {
            "intro": "Soyons lucides. Voici les failles.",
            "style": "tranchant, précis"
        },
        "protectrice": {
            "intro": "Je veux que tout reste doux. Je suis là pour veiller.",
            "style": "chaleureux, rassurant"
        }
    }

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        plugins_log = ctx.setdefault("plugins_log", [])
        dialogues = []

        for nom, profil in self.profils.items():
            intro = profil["intro"]
            voix = f"**{nom.capitalize()}** ({profil['style']}): {intro}\n→ Réponse à la question : « {message[:80]}... »"
            dialogues.append(voix)

        ctx["dialogue_facettes"] = "\n\n".join(dialogues)
        plugins_log.append("DialogueFacettesPlugin : dialogue intérieur généré")
        logger.info("[dialogue_facettes] Dialogue multi-soi activé")

        return ctx
