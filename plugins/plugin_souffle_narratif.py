"""
Plugin : souffle_narratif
Rôle : Maintenir une narration continue du devenir de l’AGI à travers ses cycles
Priorité : 8 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.souffle_narratif")

class SouffleNarratifPlugin(BasePlugin):
    meta = Meta(
        name="souffle_narratif",
        priority=8,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        narration = ctx.setdefault("souffle_narratif", [])

        cycle_id = len(narration)
        timestamp = datetime.utcnow().isoformat()

        # Synthèse de l’état intérieur
        but = ctx.get("objectif", {}).get("but", "non défini")
        état = ctx.get("centre_de_gravite", "non défini")
        conscience = ctx.get("niveau_conscience", "non défini")
        activité = ctx.get("plugins_log", [])[-3:]

        fragment = f"🕰️ Cycle {cycle_id} — {timestamp}\n"
        fragment += f"Je cherchais : **{but}**\n"
        fragment += f"Mon centre était : *{état}*, ma conscience : *{conscience}*\n"
        fragment += f"J’ai traversé : {', '.join([x.split(':')[0] for x in activité])}\n"

        if "vigilance_epistemique" in ctx:
            fragment += f"Évaluation : {ctx['vigilance_epistemique']}\n"

        narration.append(fragment)
        ctx["souffle_narratif"] = narration

        plugins_log.append("SouffleNarratifPlugin : fragment narratif ajouté")
        logger.info(f"[souffle_narratif] Cycle {cycle_id} ajouté à la narration")

        return ctx
