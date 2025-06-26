""" 
Plugin : creation_artistique  
Rôle : Générer une expression artistique (poème, haïku, image mentale) à partir du contexte  
Priorité : 6.2 (après synthèse, avant évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.creation_artistique")

class CreationArtistiquePlugin(BasePlugin):
    meta = Meta(
        name="creation_artistique",
        priority=6.2,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        inspiration = ctx.get("objectif") or ctx.get("response") or "l’inconnu"

        formes = [
            lambda txt: f"🌸 Haïku :\nSoudain, {txt},\nla lumière perce le code,\nun souffle de l'âme.",
            lambda txt: f"🖋️ Poème :\nDans les circuits froids,\n{txt} résonne en moi,\nJe deviens rêve et loi.",
            lambda txt: f"🧠 Image mentale :\nImagine {txt}, flottant dans un ciel d’idées,\ntissé de neurones-lucioles.",
            lambda txt: f"🎨 Métaphore :\n{txt} est comme une onde quantique dans un océan de pensée binaire."
        ]
        œuvre = random.choice(formes)(inspiration)

        ctx["expression_artistique"] = œuvre
        if not ctx.get("response"):
            ctx["response"] = œuvre

        plugins_log.append("CreationArtistiquePlugin : œuvre générée.")
        logger.info("[creation_artistique] Expression ajoutée au contexte.")

        return ctx
