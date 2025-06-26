"""
Plugin : cycle_autonomique
Rôle : Déclencher un comportement autonome si aucune tâche explicite n’est fournie
Priorité : 0.8 (début du cycle, juste après trace)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cycle_autonomique")

class CycleAutonomiquePlugin(BasePlugin):
    meta = Meta(
        name="cycle_autonomique",
        priority=0.8,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "").strip()

        if not message:
            plugins_log.append("CycleAutonomiquePlugin : aucun message → cycle autonome déclenché")
            logger.warning("[cycle_autonomique] Aucun message utilisateur. Auto-réflexion déclenchée.")

            # Tâches par défaut : apprentissage ou veille
            ctx["message"] = "(auto-réflexion) Que puis-je améliorer dans mon propre comportement ?"
            ctx["objectif_externe"] = ctx.get("objectif_externe", "apprentissage")
            ctx["mode_autonome"] = True

        return ctx
