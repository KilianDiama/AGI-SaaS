# plugins/plugin_clustering_vectoriel.py

"""
Plugin : plugin_clustering_vectoriel
Rôle : Réalise un clustering vectoriel (KMeans) sur des données textuelles (souvenirs, idées, réponses...)
Priorité : 2.9 (juste avant raisonnement ou fusion)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logger = logging.getLogger("plugin.clustering_vectoriel")

class PluginClusteringVectoriel(BasePlugin):
    meta = Meta(
        name="plugin_clustering_vectoriel",
        priority=2.9,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        données: List[str] = ctx.get("clustering_data", [])

        if not données or len(données) < 3:
            ctx.setdefault("plugins_log", []).append("plugin_clustering_vectoriel : pas assez de données à clusteriser.")
            return ctx

        try:
            vect = TfidfVectorizer(stop_words="french")
            matrice = vect.fit_transform(données)

            n_clusters = min(5, len(données) // 2)  # Adaptatif
            kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
            labels = kmeans.fit_predict(matrice)

            clusters = {}
            for i, label in enumerate(labels):
                clusters.setdefault(label, []).append(données[i])

            ctx["clustering_result"] = clusters
            ctx.setdefault("plugins_log", []).append(f"plugin_clustering_vectoriel : {n_clusters} groupes générés.")
            logger.info(f"[clustering_vectoriel] Clusters : {list(clusters.keys())}")

        except Exception as e:
            ctx["clustering_result"] = {}
            ctx.setdefault("plugins_log", []).append(f"plugin_clustering_vectoriel : erreur → {e}")
            logger.error(f"[clustering_vectoriel] Erreur : {e}")

        return ctx
