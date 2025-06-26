""" 
Plugin : synthese_memoire  
Rôle : Générer un résumé des souvenirs mémorisés pour identifier des motifs, thèmes et apprentissages  
Priorité : 5.7 (juste après invention, avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from collections import Counter
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.synthese_memoire")

class SyntheseMemoirePlugin(BasePlugin):
    meta = Meta(
        name="synthese_memoire",
        priority=5.7,
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
                logger.warning(f"[synthese_memoire] Erreur lecture mémoire : {e}")
        return []

    def resumer_memoire(self, memoire):
        if not memoire:
            return "⚠️ Aucune mémoire enregistrée."

        # Sécurisation : forcer les objectifs à être du texte
        objectifs = [str(s.get("objectif", "")) for s in memoire if "objectif" in s]
        lecons = [str(s.get("lecon", "")) for s in memoire if s.get("lecon")]

        top_objectifs = Counter(objectifs).most_common(3)
        resume_obj = "\n".join([f"- {o} ({n}x)" for o, n in top_objectifs])

        resume = (
            f"📚 Synthèse de la mémoire :\n"
            f"Objectifs fréquents :\n{resume_obj}\n\n"
            f"Exemples de leçons apprises :\n"
        )
        resume += "\n".join(f"• {l[:100]}" for l in lecons[-3:])
        return resume

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        memoire = self.charger_memoire()
        synthese = self.resumer_memoire(memoire)

        ctx["synthese_memoire"] = synthese
        if not ctx.get("response"):
            ctx["response"] = synthese

        plugins_log.append("SyntheseMemoirePlugin : synthèse de mémoire générée.")
        logger.info("[synthese_memoire] Synthèse produite.")

        return ctx
