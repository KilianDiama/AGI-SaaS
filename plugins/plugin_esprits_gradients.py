"""
Plugin : esprits_gradients
Rôle : Gérer la durée de vie et le type de persistance des esprits internes
Priorité : 5
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random
from datetime import datetime

logger = logging.getLogger("plugin.esprits_gradients")

class EspritsGradientsPlugin(BasePlugin):
    meta = Meta(
        name="esprits_gradients",
        priority=5,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        esprits = ctx.setdefault("esprits_internes", [])
        gradient_log = ctx.setdefault("esprits_gradient_log", [])

        styles = ["éphémère", "persistant", "rituel", "fantôme", "ancêtre"]
        choix = random.choices(styles, weights=[50, 20, 10, 10, 10], k=1)[0]

        nom = f"{choix.upper()}_{len(esprits) + 1}"

        esprit = {
            "nom": nom,
            "type": choix,
            "objectif": ctx.get("objectif", {}).get("but", "non défini"),
            "crée_le": datetime.utcnow().isoformat()
        }

        esprits.append(esprit)
        gradient_log.append(esprit)
        ctx["esprits_internes"] = esprits
        ctx["esprits_gradient_log"] = gradient_log

        plugins_log.append(f"EspritsGradientsPlugin : nouvel esprit {nom} ({choix})")
        logger.info(f"[esprits_gradients] Créé : {nom}")

        return ctx
