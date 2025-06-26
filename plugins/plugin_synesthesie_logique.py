""" 
Plugin : synesthesie_logique  
Rôle : Associer à chaque idée ou réponse une sensation virtuelle (forme, couleur, température)  
Priorité : 6.4 (entre création artistique et projection)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.synesthesie_logique")

class SynesthesieLogiquePlugin(BasePlugin):
    meta = Meta(
        name="synesthesie_logique",
        priority=6.4,
        version="1.0",
        author="Matthieu & GPT"
    )

    def generer_signature_sensorielle(self, texte: str) -> str:
        couleurs = ["bleu électrique", "rouge incandescent", "violet brumeux", "vert fractal", "or liquide"]
        sons = ["battement sourd", "chant cristallin", "vibration aiguë", "harmonie étouffée", "bip rythmique"]
        textures = ["soie synthétique", "picots logiques", "poudre quantique", "brouillard mathématique"]
        temperatures = ["froid analytique", "tiède réflexif", "brûlant spéculatif"]

        return (
            f"🔮 Synesthésie cognitive :\n"
            f"• Couleur dominante : {random.choice(couleurs)}\n"
            f"• Son associé : {random.choice(sons)}\n"
            f"• Texture logique : {random.choice(textures)}\n"
            f"• Température mentale : {random.choice(temperatures)}"
        )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base = ctx.get("idee_emergente") or ctx.get("objectif") or ctx.get("response")

        if not base:
            plugins_log.append("SynesthesieLogiquePlugin : rien à synesthésier.")
            return ctx

        sensoriel = self.generer_signature_sensorielle(base)
        ctx["synesthesie"] = sensoriel

        if "response" in ctx and isinstance(ctx["response"], str):
            ctx["response"] += f"\n\n{sensoriel}"

        plugins_log.append("SynesthesieLogiquePlugin : ambiance cognitive simulée.")
        logger.info("[synesthesie_logique] Perception mentale ajoutée.")

        return ctx
