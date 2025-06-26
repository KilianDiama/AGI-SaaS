# plugins/plugin_analyse_semantique.py

"""
Plugin : plugin_analyse_semantique
Rôle : Analyser le message utilisateur → ton, thème, intention implicite
Priorité : 1.4 (après détection d’intention mais avant réflexion)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.analyse_semantique")

TONS = {
    "neutre": ["ok", "d’accord", "entendu", "hmm"],
    "positif": ["merci", "génial", "super", "cool", "parfait", "top"],
    "colère": ["nul", "ça sert à rien", "j’en ai marre", "pourquoi ça marche pas"],
    "tristesse": ["je suis triste", "fatigué", "déprimé", "j’abandonne"]
}

THEMES = {
    "ia": ["intelligence", "machine", "deep learning", "ia", "agent"],
    "dev": ["code", "python", "bug", "erreur", "fonction", "script"],
    "vie": ["manger", "dormir", "espoir", "bonheur", "sens", "souffrance"],
    "projet": ["plan", "objectif", "mission", "tâche", "workflow", "projet"]
}

class PluginAnalyseSemantique(BasePlugin):
    meta = Meta(
        name="plugin_analyse_semantique",
        priority=1.4,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        msg = ctx.get("message", "").lower()
        if not msg.strip():
            ctx.setdefault("plugins_log", []).append("plugin_analyse_semantique : message vide")
            return ctx

        ton = self.detecter_ton(msg)
        theme = self.detecter_theme(msg)

        ctx["analyse_semantique"] = {
            "ton": ton,
            "theme": theme,
            "emotif": ton in ("colère", "tristesse", "positif"),
            "technique": theme in ("ia", "dev")
        }

        ctx.setdefault("plugins_log", []).append(f"plugin_analyse_semantique : ton={ton}, thème={theme}")
        logger.info(f"[analyse_semantique] Ton : {ton}, Thème : {theme}")
        return ctx

    def detecter_ton(self, message):
        for ton, mots in TONS.items():
            if any(m in message for m in mots):
                return ton
        return "neutre"

    def detecter_theme(self, message):
        scores = {}
        for theme, mots in THEMES.items():
            scores[theme] = sum(1 for m in mots if m in message)
        return max(scores, key=scores.get) if any(scores.values()) else "inconnu"
