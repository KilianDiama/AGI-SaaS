# plugins/plugin_vector_store.py

"""
Plugin : plugin_vector_store
Rôle : Stocker et retrouver des textes en mémoire vectorielle (sémantique)
Priorité : 1.9 (avant clustering, raisonnement, synthèse)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import json
import os

logger = logging.getLogger("plugin.vector_store")

DATA_PATH = "/mnt/data/vector_memory.json"

class PluginVectorStore(BasePlugin):
    meta = Meta(
        name="plugin_vector_store",
        priority=1.9,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        nouveau = ctx.get("memoire_vectorielle_add")
        requete = ctx.get("memoire_vectorielle_query")

        mémoire = self._charger_memoire()

        if nouveau:
            mémoire.append(nouveau)
            self._sauver_memoire(mémoire)
            logger.info("[vector_store] Ajouté à la mémoire vectorielle.")
            ctx.setdefault("plugins_log", []).append("plugin_vector_store : ajout effectué.")

        if requete:
            resultat = self._retrouver_plus_proche(requete, mémoire)
            ctx["memoire_vectorielle_result"] = resultat
            logger.info("[vector_store] Résultat de la requête vectorielle injecté.")
            ctx.setdefault("plugins_log", []).append("plugin_vector_store : similarité calculée.")

        return ctx

    def _charger_memoire(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"[vector_store] Erreur chargement : {e}")
        return []

    def _sauver_memoire(self, memoire):
        try:
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(memoire, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[vector_store] Erreur sauvegarde : {e}")

    def _retrouver_plus_proche(self, texte, corpus):
        if not corpus:
            return []

        vect = TfidfVectorizer().fit(corpus + [texte])
        vecteurs = vect.transform(corpus + [texte])
        simil = cosine_similarity(vecteurs[-1], vecteurs[:-1]).flatten()

        top_indices = simil.argsort()[::-1][:3]
        return [{"texte": corpus[i], "score": float(simil[i])} for i in top_indices if simil[i] > 0.1]
