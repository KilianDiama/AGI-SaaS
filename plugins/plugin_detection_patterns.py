""" 
Plugin : detection_patterns  
Rôle : Détecter les motifs cognitifs récurrents dans la mémoire long terme  
Priorité : 5.8 (juste après synthèse mémoire, avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from collections import Counter
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.detection_patterns")

class DetectionPatternsPlugin(BasePlugin):
    meta = Meta(
        name="detection_patterns",
        priority=5.8,
        version="1.1",  # version corrigée
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self):
        if os.path.exists(self.MEMOIRE_PATH):
            try:
                with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[detection_patterns] Erreur lecture mémoire : {e}")
        return []

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        memoire = self.charger_memoire()

        if not memoire:
            ctx["patterns_detectes"] = "⚠️ Aucune mémoire enregistrée pour analyse."
            return ctx

        # Sécurisation : conversion explicite en texte
        objectifs = [str(s.get("objectif", "")) for s in memoire]
        reponses = [str(s.get("reponse", "")) for s in memoire]

        top_objectifs = Counter(objectifs).most_common(2)
        top_mots = Counter(" ".join(objectifs).split()).most_common(5)

        pattern_texte = (
            "🧬 Motifs détectés dans les souvenirs :\n"
            f"🎯 Objectifs fréquents : {', '.join([f'{o} ({n}x)' for o, n in top_objectifs])}\n"
            f"🔁 Mots-clés dominants : {', '.join([m for m, _ in top_mots])}"
        )

        ctx["patterns_detectes"] = pattern_texte
        if not ctx.get("response"):
            ctx["response"] = pattern_texte

        plugins_log.append("DetectionPatternsPlugin : motifs cognitifs extraits.")
        logger.info("[detection_patterns] Motifs ajoutés au contexte.")

        return ctx
