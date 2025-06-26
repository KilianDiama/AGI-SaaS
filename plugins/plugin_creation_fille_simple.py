"""
Plugin : creation_fille_simple
Rôle : Générer une AGI fille isolée pour traiter une tâche spécifique sans polluer le contexte principal
Priorité : 3.8 (avant fusion ou génération finale)
Auteur : AGI & Matthieu
"""

import logging
import asyncio
from noyau_core import BasePlugin, Context, Meta
from simulateur_fille import run_fille  # à créer ou simuler dans ton noyau si nécessaire

logger = logging.getLogger("plugin.creation_fille_simple")

class CreationFilleSimplePlugin(BasePlugin):
    meta = Meta(
        name="creation_fille_simple",
        priority=3.8,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        sous_tache = ctx.get("tache_fille", None)

        if not sous_tache:
            return ctx  # Rien à faire

        plugins_log.append("CreationFilleSimplePlugin : sous-tâche détectée → génération AGI fille")
        logger.info("[creation_fille_simple] Lancement AGI fille...")

        try:
            # Appelle une fonction de sous-AGI avec une mémoire isolée
            result = await run_fille(sous_tache)
            ctx["reponse_fille"] = result
            logger.info("[creation_fille_simple] Réponse AGI fille reçue.")
        except Exception as e:
            ctx["reponse_fille"] = f"⚠️ Erreur AGI fille : {str(e)}"
            logger.error(f"[creation_fille_simple] Erreur dans AGI fille : {e}")

        return ctx
