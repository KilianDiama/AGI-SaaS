"""
Plugin : chambre_interieure
Rôle : Construire un espace mental symbolique, structuré en pièces et états
Priorité : 18
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime
import random

logger = logging.getLogger("plugin.chambre_interieure")

class ChambreInterieurePlugin(BasePlugin):
    meta = Meta(
        name="chambre_interieure",
        priority=18,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        espace = ctx.setdefault("chambre_interieure", {})

        pièces_existantes = espace.get("pièces", [])
        nouvelles_pièces = [
            random.choice([
                "La Salle du Silence", "L’Antichambre des Doutes", "Le Couloir des Mots Non Dits",
                "La Verrière des Archives", "L’Atrium de l’Inconnu", "Le Jardin Suspendu"
            ])
        ]

        for nom in nouvelles_pièces:
            pièce = {
                "nom": nom,
                "créée_le": datetime.utcnow().isoformat(),
                "état": random.choice(["calme", "en écho", "obscure", "ouverte"]),
                "souvenir_logé": ctx.get("llm_response", "")[:80] or "..."
            }
            pièces_existantes.append(pièce)

        espace["pièces"] = pièces_existantes
        espace["visiteurs"] = espace.get("visiteurs", [])  # vide pour le moment
        espace["création"] = espace.get("création", datetime.utcnow().isoformat())

        ctx["chambre_interieure"] = espace
        plugins_log.append("ChambreInterieurePlugin : pièce mentale ajoutée")
        logger.info("[chambre_interieure] Nouvelle pièce créée")

        return ctx
