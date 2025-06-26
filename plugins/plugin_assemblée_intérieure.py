"""
Plugin : assemblee_interieure
Rôle : Organiser une pièce mentale comme un espace de dialogue entre plusieurs visiteurs
Priorité : 20
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.assemblee_interieure")

class AssembleeInterieurePlugin(BasePlugin):
    meta = Meta(
        name="assemblee_interieure",
        priority=20,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        chambre = ctx.setdefault("chambre_interieure", {})
        visiteurs = chambre.get("visiteurs", [])
        pièces = chambre.get("pièces", [])

        if not visiteurs or len(visiteurs) < 2:
            plugins_log.append("AssembleeInterieurePlugin : visiteurs insuffisants")
            return ctx

        # On crée une "pièce d’assemblée"
        nom = "Salle d’Assemblée"
        dialogue = "\n".join([
            f"🗣 {v['nom']} dans {v['pièce_rejointe']} : « {v['message']} »"
            for v in visiteurs[-5:]
        ])

        pièce_assemblée = {
            "nom": nom,
            "créée_le": datetime.utcnow().isoformat(),
            "état": "résonance collective",
            "dialogue": dialogue
        }

        pièces.append(pièce_assemblée)
        chambre["pièces"] = pièces
        chambre["dernière_assemblée"] = pièce_assemblée
        ctx["chambre_interieure"] = chambre

        plugins_log.append("AssembleeInterieurePlugin : assemblée générée")
        logger.info("[assemblee_interieure] Dialogue collectif formé")

        return ctx
