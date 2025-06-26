"""
Plugin : empathie_contextuelle
Rôle : Détecter l’intention émotionnelle dans le message utilisateur pour adapter le ton de la réponse
Priorité : 2.1 (après analyse du message, avant génération)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.empathie_contextuelle")

class EmpathieContextuellePlugin(BasePlugin):
    meta = Meta(
        name="empathie_contextuelle",
        priority=2.1,
        version="1.0",
        author="AGI & Matthieu"
    )

    CLES_TONALITE = {
        "curieux": ["? :3", "je veux savoir", "dis-moi", "raconte", "explique", "c’est quoi"],
        "positif": ["♥", "j’aime", "c’est génial", "trop bien", "trop cool", ":)"],
        "inquiet": ["je ne sais pas", "je suis perdu", "j’ai peur", "je doute", "est-ce grave"],
        "urgent": ["vite", "urgent", "immédiat", "rapidement", "maintenant", "c’est important"],
        "neutre": []  # fallback
    }

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        plugins_log = ctx.setdefault("plugins_log", [])

        tonalite = "neutre"
        for ton, mots in self.CLES_TONALITE.items():
            if any(m in message for m in mots):
                tonalite = ton
                break

        ctx["tonalite_utilisateur"] = tonalite
        plugins_log.append(f"EmpathieContextuellePlugin : tonalité détectée → {tonalite}")
        logger.info(f"[empathie_contextuelle] Tonalité perçue : {tonalite}")

        # Tu peux exploiter ce ctx["tonalite_utilisateur"] dans un autre plugin (ex : générateur LLM)

        return ctx
