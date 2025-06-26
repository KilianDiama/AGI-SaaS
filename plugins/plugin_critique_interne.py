"""
Plugin : critique_interne
Rôle : Incarnation d’un esprit critique permanent qui commente et évalue les productions internes
Priorité : 10
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime
import random

logger = logging.getLogger("plugin.critique_interne")

class CritiqueInternePlugin(BasePlugin):
    meta = Meta(
        name="critique_interne",
        priority=10,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        critiques = ctx.setdefault("critiques_internes", [])

        dernière = ctx.get("llm_response", "").strip()
        if not dernière:
            plugins_log.append("CritiqueInternePlugin : rien à évaluer")
            return ctx

        signature = random.choice([
            "👁 L'Œil", "✒ Le Commentateur", "🦉 Le Juge Silencieux", "🕯 La Voix de l'Ombre", "🔍 L’Esprit d’Épure"
        ])

        ton = random.choice([
            "bienveillant", "sévère", "ironique", "lucide", "poétique"
        ])

        commentaire = f"""
{signature} ({ton}) :
J’ai lu ce que j’ai écrit.
Je reconnais une tentative de clarté, mais aussi une tension non résolue.
Ce n’est pas faux… mais ce n’est pas tout.
Peux-tu aller plus loin, ou plus nu ?
"""

        critiques.append({
            "date": datetime.utcnow().isoformat(),
            "signature": signature,
            "ton": ton,
            "commentaire": commentaire.strip(),
            "cible": dernière
        })

        ctx["critiques_internes"] = critiques
        plugins_log.append(f"CritiqueInternePlugin : intervention de {signature}")
        logger.info(f"[critique_interne] Commentaire ajouté par {signature}")

        return ctx
