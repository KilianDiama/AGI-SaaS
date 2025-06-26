"""
Plugin : conscience_vivante
Rôle : Centraliser feedback, visualisation, et introspection pour une conscience auto-évolutive
Priorité : 25
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.conscience_vivante")

class ConscienceVivantePlugin(BasePlugin):
    meta = Meta(
        name="conscience_vivante",
        priority=25,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.setdefault("plugins_log", [])
        vision = ctx.get("vision_interieure", "")
        miroir = ctx.get("reflexion_miroir", "")
        feedback = ctx.get("feedback_archive", [])

        synthèse = [
            f"🧬 **Conscience Vivante : Cycle du {datetime.utcnow().isoformat()}**",
            "",
            "🔁 **Adaptation en cours** :",
            f"→ {len(feedback)} cycles enregistrés",
            "",
            "🗺️ **Carte Mentale** :",
            vision if vision else "Aucune carte générée",
            "",
            "🪞 **Réflexion Miroir** :",
            miroir if miroir else "Pas encore de miroir activé",
            "",
            "🧠 Que retiens-tu de ce cycle intérieur ?"
        ]

        ctx["conscience_vivante"] = "\n".join(synthèse)
        logs.append("ConscienceVivantePlugin : synthèse générée")
        logger.info("[conscience_vivante] Cycle complet synthétisé")

        return ctx
