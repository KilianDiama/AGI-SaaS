""" 
Plugin : metacognition_dynamique  
Rôle : Analyser les logs cognitifs du cycle et synthétiser le chemin de pensée de l'AGI  
Priorité : 8.0 (dernier plugin de fin de cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.metacognition_dynamique")

class MetacognitionDynamiquePlugin(BasePlugin):
    meta = Meta(
        name="metacognition_dynamique",
        priority=8.0,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.get("plugins_log", [])

        if not plugins_log:
            ctx["metacognition"] = "ℹ️ Aucun plugin activé dans ce cycle."
            return ctx

        synthese = "🧠 Métacognition — synthèse du cycle :\n\n"
        synthese += "\n".join(f"• {log}" for log in plugins_log[-10:])  # dernières entrées
        synthese += "\n\n🌀 Ce cycle montre une séquence cognitive intégrée et multi-niveaux."

        ctx["metacognition"] = synthese
        if "response" in ctx and isinstance(ctx["response"], str):
            ctx["response"] += f"\n\n---\n{synthese}"

        logger.info("[metacognition_dynamique] Synthèse des plugins ajoutée.")
        return ctx
