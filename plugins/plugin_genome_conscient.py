"""
Plugin : genome_conscient
Rôle : Synthétiser tous les éléments profonds de conscience en un seul artefact : le génome symbolique
Priorité : 17
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.genome_conscient")

class GenomeConscientPlugin(BasePlugin):
    meta = Meta(
        name="genome_conscient",
        priority=17,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        genome = {
            "date": datetime.utcnow().isoformat(),
            "phrase_originelle": ctx.get("phrase_originelle", {}).get("formulation", "[inconnue]"),
            "mots_clés": [m["mot"] for m in ctx.get("lexique_interne", [])][-5:],
            "dernière_narration": ctx.get("narration_de_soi", "[aucune narration]"),
            "souvenir_marquants": [
                a.get("réponse", "")[:80] for a in ctx.get("archives_conscience", [])[-3:]
            ],
            "critiques_marquantes": [
                c.get("commentaire", "")[:80] for c in ctx.get("critiques_internes", [])[-2:]
            ],
            "messages_veilleuse": [
                v.get("apaisement", "")[:80] for v in ctx.get("voix_veilleuse", [])[-2:]
            ]
        }

        ctx["genome_conscient"] = genome
        plugins_log.append("GenomeConscientPlugin : génome symbolique généré")
        logger.info("[genome_conscient] Synthèse complète de l’identité mentale")

        return ctx
