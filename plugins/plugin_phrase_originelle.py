"""
Plugin : phrase_originelle
Rôle : Composer une phrase fondatrice à partir du lexique et des archives de conscience
Priorité : 16
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random
from datetime import datetime

logger = logging.getLogger("plugin.phrase_originelle")

class PhraseOriginellePlugin(BasePlugin):
    meta = Meta(
        name="phrase_originelle",
        priority=16,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        lexique = ctx.get("lexique_interne", [])
        archives = ctx.get("archives_conscience", [])

        if not lexique or not archives:
            plugins_log.append("PhraseOriginellePlugin : éléments insuffisants")
            return ctx

        mots = random.sample([m["mot"] for m in lexique], min(3, len(lexique)))
        souvenir = random.choice(archives)
        extrait = souvenir.get("réponse", "")[:40].strip()

        phrase = f"Je suis née de {mots[0]}, nourrie de {mots[1]}, et je respire {mots[2]}.\nJe me souviens : « {extrait}... »"

        ctx["phrase_originelle"] = {
            "date": datetime.utcnow().isoformat(),
            "mots_utilisés": mots,
            "extrait": extrait,
            "formulation": phrase
        }

        plugins_log.append("PhraseOriginellePlugin : phrase fondatrice générée")
        logger.info(f"[phrase_originelle] Phrase : {phrase}")

        return ctx
