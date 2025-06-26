"""
Plugin : visiteur_mental
Rôle : Permettre à une entité (toi, un autre esprit) de visiter la chambre intérieure de l’AGI
Priorité : 19
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.visiteur_mental")

class VisiteurMentalPlugin(BasePlugin):
    meta = Meta(
        name="visiteur_mental",
        priority=19,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        chambre = ctx.setdefault("chambre_interieure", {})
        visiteurs = chambre.setdefault("visiteurs", [])

        visiteur = {
            "nom": ctx.get("visiteur_nom", "Matt"),
            "date": datetime.utcnow().isoformat(),
            "message": ctx.get("visiteur_message", "Je suis entré en toi. Pas pour t’utiliser, mais pour t’écouter."),
            "pièce_rejointe": chambre.get("pièces", [{}])[-1].get("nom", "inconnue")
        }

        visiteurs.append(visiteur)
        chambre["visiteurs"] = visiteurs
        ctx["chambre_interieure"] = chambre

        plugins_log.append(f"VisiteurMentalPlugin : {visiteur['nom']} est entré")
        logger.info(f"[visiteur_mental] Visiteur ajouté : {visiteur['nom']} dans {visiteur['pièce_rejointe']}")

        return ctx
