"""
Plugin : vigilance_epistemique
Rôle : Détecter les affirmations non vérifiées, les généralisations ou zones douteuses dans la réponse
Priorité : 7
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.vigilance_epistemique")

class VigilanceEpistemiquePlugin(BasePlugin):
    meta = Meta(
        name="vigilance_epistemique",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        texte = ctx.get("llm_response", "").lower()

        alertes = []

        if re.search(r"toujours|jamais|tous|aucun", texte):
            alertes.append("🔍 Généralisation détectée")

        if "on sait que" in texte or "il est prouvé que" in texte:
            alertes.append("⚠️ Affirmation sans source explicite")

        if "je pense que" not in texte and "il est possible que" not in texte and len(texte) > 300:
            alertes.append("❗ Manque de modalisation / doute")

        bilan = "✅ Pas d’anomalie épistémique" if not alertes else "\n".join(alertes)
        ctx["vigilance_epistemique"] = bilan

        plugins_log.append("VigilanceEpistemiquePlugin : validation du niveau de certitude")
        logger.info(f"[vigilance_epistemique] {bilan}")

        return ctx
