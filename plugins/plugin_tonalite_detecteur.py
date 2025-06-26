import logging
from noyau_core import BasePlugin, Context, Meta
import re

logger = logging.getLogger("plugin.tonalite")

class PluginTonaliteDetecteur(BasePlugin):
    meta = Meta(
        name="plugin_tonalite_detecteur",
        version="1.0",
        priority=1.4,  # Avant raisonneur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").lower()
        tonalite = "neutre"

        if any(x in message for x in ["merci", "super", "génial", "trop bien", "parfait", "cool"]):
            tonalite = "positive"
        elif any(x in message for x in ["je suis triste", "fatigué", "déçu", "nul", "aucune réponse"]):
            tonalite = "négative"
        elif any(x in message for x in ["hein", "quoi", "tu m’écoutes ?", "allo"]):
            tonalite = "frustrée"
        elif "?" in message:
            tonalite = "curieuse"

        ctx["tonalite_utilisateur"] = tonalite
        ctx.setdefault("plugins_log", []).append(f"PluginTonaliteDetecteur : tonalité détectée → {tonalite}")
        logger.info(f"[tonalité] Détectée : {tonalite}")

        return ctx
