"""
Plugin : gestion_priorites
Rôle : Organiser les tâches mentales par priorité et reporter les moins urgentes
Priorité : 2.3 (avant réflexion interne, mémoire ou génération)
Auteur : AGI & Matthieu
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.gestion_priorites")

class GestionPrioritesPlugin(BasePlugin):
    meta = Meta(
        name="gestion_priorites",
        priority=2.3,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire_priorites = ctx.setdefault("priorites", [])

        message = ctx.get("message", "")
        priorite = 1.0  # Valeur par défaut

        # Détection simple : mots clés → ajuster la priorité
        if any(k in message.lower() for k in ["urgent", "vite", "important"]):
            priorite = 3.0
        elif any(k in message.lower() for k in ["plus tard", "après", "en pause"]):
            priorite = 0.5
        elif any(k in message.lower() for k in ["expérimental", "idée", "test"]):
            priorite = 1.5

        memoire_priorites.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "priorite": priorite
        })

        ctx["priorites"] = sorted(memoire_priorites, key=lambda x: -x["priorite"])
        plugins_log.append(f"GestionPrioritesPlugin : message noté avec priorité {priorite}")
        logger.info(f"[gestion_priorites] Message priorisé → {priorite}")

        return ctx
