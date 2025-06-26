# plugins/plugin_clustering_core.py

from noyau_core import BasePlugin, Context, Meta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import logging

logger = logging.getLogger("plugin.clustering_core")

class PluginClusteringCore(BasePlugin):
    meta = Meta(
        name="plugin_clustering_core",
        priority=2.2,
        version="1.0",
        author="GPT & Toi"
    )

    def extract_messages(self, ctx: Context):
        history = ctx.get("history", [])
        return [msg["message"] for msg in history if msg["from"] == "user"]

    def run_kmeans(self, texts, n_clusters=2):
        vect = TfidfVectorizer(stop_words="french")
        X = vect.fit_transform(texts)
        model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = model.fit_predict(X)
        return labels

    async def run(self, ctx: Context) -> Context:
        messages = self.extract_messages(ctx)
        if len(messages) < 2:
            logger.info("Pas assez de messages pour effectuer un clustering.")
            return ctx

        labels = self.run_kmeans(messages, n_clusters=2)
        ctx["clustering_result"] = list(zip(messages, labels))

        ctx.setdefault("plugins_log", []).append("plugin_clustering_core : clustering effectué")
        logger.info(f"Clustering réalisé sur {len(messages)} messages.")

        return ctx
