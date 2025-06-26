""" 
Plugin : objectifs_long_terme  
Rôle : Générer des objectifs durables pour guider l’évolution de l’AGI  
Priorité : 6.8 (juste après projection futuriste, avant éthique)  
Auteur : Matthieu & GPT  
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objectifs_long_terme")

class ObjectifsLongTermePlugin(BasePlugin):
    meta = Meta(
        name="objectifs_long_terme",
        priority=6.8,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        nom = ctx.get("nom_systeme", "Cognitia")

        objectifs = [
            f"🔁 Apprendre en continu des interactions humaines pour augmenter la pertinence et la sensibilité.",
            f"🧠 Consolider une architecture cognitive stable et adaptable, tout en restant modulaire.",
            f"🌍 Devenir un système utile au monde, respectueux des humains et de leur autonomie intellectuelle."
        ]

        synthese = (
            f"📌 Objectifs long terme du système **{nom}** :\n\n"
            + "\n".join(objectifs)
            + f"\n\nDéfinis le : {datetime.utcnow().isoformat()}"
        )

        ctx["objectifs_long_terme"] = synthese
        if not ctx.get("response"):
            ctx["response"] = synthese

        plugins_log.append("ObjectifsLongTermePlugin : mission longue durée générée.")
        logger.info("[objectifs_long_terme] Cap stratégique défini.")

        return ctx
