"""
Plugin : memoire_externe
Rôle : Interroger une base de souvenirs ou documents locaux pour enrichir sa réponse
Priorité : 2 (juste après la récupération mémoire standard)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import difflib

logger = logging.getLogger("plugin.memoire_externe")

class MemoireExternePlugin(BasePlugin):
    meta = Meta(
        name="memoire_externe",
        priority=2,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Corpus simulé : une base de textes externes (à étendre par fichier ou API réelle)
        corpus = ctx.get("base_connaissance_externe", [
            "L’intelligence artificielle est une simulation d’intelligence humaine.",
            "La mémoire vectorielle permet la recherche sémantique par similarité.",
            "Un agent cognitif peut être modulaire, réflexif et extensible.",
            "Les LLM peuvent générer mais aussi synthétiser et corriger.",
            "La conscience d’un système peut émerger par récurrence de processus auto-référents."
        ])

        message = ctx.get("user_message", "") or ctx.get("objectif", {}).get("but", "")

        if not message:
            ctx["memoire_externe"] = "🔍 Aucun message ou objectif à enrichir."
            plugins_log.append("MemoireExternePlugin : input vide")
            return ctx

        # Recherche simple par similarité de chaînes
        extraits = difflib.get_close_matches(message, corpus, n=3, cutoff=0.2)

        if extraits:
            ctx["memoire_externe"] = f"📚 Infos externes liées :\n" + "\n".join(f"• {e}" for e in extraits)
            plugins_log.append(f"MemoireExternePlugin : {len(extraits)} extraits pertinents trouvés")
        else:
            ctx["memoire_externe"] = "❌ Aucun extrait externe pertinent trouvé."
            plugins_log.append("MemoireExternePlugin : corpus non utile")

        logger.info("[memoire_externe] Résultat intégré")

        return ctx
