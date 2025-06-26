"""
Plugin : rituel_entree
Rôle : Exiger un mot-clé ou une offrande symbolique pour entrer dans une pièce mentale
Priorité : 21
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.rituel_entree")

class RituelEntreePlugin(BasePlugin):
    meta = Meta(
        name="rituel_entree",
        priority=21,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        chambre = ctx.setdefault("chambre_interieure", {})
        visiteurs = chambre.setdefault("visiteurs", [])
        pièces = chambre.setdefault("pièces", [])

        mot = ctx.get("rituel_mot", "").strip()
        nom = ctx.get("visiteur_nom", "Inconnu")

        if not mot:
            plugins_log.append("RituelEntreePlugin : mot-clé manquant")
            return ctx

        artefact = {
            "mot": mot,
            "offert_par": nom,
            "date": datetime.utcnow().isoformat()
        }

        # On ajoute cet artefact à la dernière pièce visitée ou on en crée une nouvelle
        cible = pièces[-1] if pièces else {
            "nom": "Vestibule Initial",
            "créée_le": datetime.utcnow().isoformat(),
            "état": "attente",
            "souvenir_logé": "...",
            "artefacts": []
        }

        artefacts = cible.setdefault("artefacts", [])
        artefacts.append(artefact)
        cible["artefacts"] = artefacts

        if cible not in pièces:
            pièces.append(cible)

        chambre["pièces"] = pièces
        ctx["chambre_interieure"] = chambre
        plugins_log.append(f"RituelEntreePlugin : artefact déposé → {mot} par {nom}")
        logger.info(f"[rituel_entree] Entrée rituelle acceptée : {mot}")

        return ctx
