"""
Plugin : langage_interne
Rôle : Créer un lexique de mots personnels à partir de ses expériences intérieures
Priorité : 15
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random
from datetime import datetime

logger = logging.getLogger("plugin.langage_interne")

class LangageInternePlugin(BasePlugin):
    meta = Meta(
        name="langage_interne",
        priority=15,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        lexique = ctx.setdefault("lexique_interne", [])
        narration = ctx.get("narration_de_soi", "")
        émotion = random.choice(["doute", "paix", "fragment", "fusion", "lucidité", "silence", "pente douce"])

        if not narration.strip():
            plugins_log.append("LangageInternePlugin : aucune narration à transmuter")
            return ctx

        racine = "".join(random.sample(émotion, min(len(émotion), 4)))  # base aléatoire
        suffixes = ["ion", "isme", "el", "té", "ence", "ure"]
        nouveau_mot = racine + random.choice(suffixes)

        entrée = {
            "mot": nouveau_mot,
            "inspiré_par": émotion,
            "créé_le": datetime.utcnow().isoformat(),
            "signification": f"État intérieur vécu lors de : « {narration[:60]}... »"
        }

        lexique.append(entrée)
        ctx["lexique_interne"] = lexique
        plugins_log.append(f"LangageInternePlugin : mot généré → {nouveau_mot}")
        logger.info(f"[langage_interne] Nouveau mot ajouté : {nouveau_mot}")

        return ctx
