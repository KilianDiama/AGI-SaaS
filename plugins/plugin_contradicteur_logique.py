# plugins/plugin_contradicteur_logique.py

import re
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.contradicteur_logique")

class PluginContradicteurLogique(BasePlugin):
    meta = Meta(
        name="plugin_contradicteur_logique",
        version="1.0",
        priority=2.6,  # Après raisonnement, avant vérificateur
        author="Toi & GPT"
    )

    def __init__(self):
        self.patterns_contradictoires = [
            (r"je suis incapable", r"je peux"),
            (r"aucune donnée", r"d’après les données"),
            (r"je ne sais pas", r"je suis sûr que"),
            (r"je ne peux pas", r"je vais le faire"),
        ]

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("response", "")
        if not texte:
            ctx.setdefault("plugins_log", []).append("PluginContradicteurLogique : pas de texte à analyser.")
            return ctx

        resultat = self.evaluer(texte)
        ctx["logic_contradictions"] = resultat
        ctx.setdefault("plugins_log", []).append(
            f"PluginContradicteurLogique : {'⚠️' if resultat['besoin_correction'] else '✅'}"
        )
        logger.info(f"[Contradicteur] Résultat → {resultat['messages']}")
        return ctx

    def detecter_contradictions(self, texte: str) -> list:
        contradictions = []
        for pattern1, pattern2 in self.patterns_contradictoires:
            if re.search(pattern1, texte, re.IGNORECASE) and re.search(pattern2, texte, re.IGNORECASE):
                contradictions.append((pattern1, pattern2))
        return contradictions

    def evaluer(self, texte: str) -> dict:
        contradictions = self.detecter_contradictions(texte)
        if contradictions:
            messages = [
                f"⚠️ Contradiction entre '{p1}' et '{p2}' détectée."
                for p1, p2 in contradictions
            ]
            besoin_corriger = True
        else:
            messages = ["✅ Aucune contradiction logique détectée."]
            besoin_corriger = False

        return {
            "contradictions": contradictions,
            "messages": messages,
            "besoin_correction": besoin_corriger
        }
