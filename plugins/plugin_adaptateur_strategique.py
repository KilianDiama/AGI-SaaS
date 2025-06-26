# plugins/plugin_adaptateur_strategique.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin_adaptateur_strategique")

class PluginAdaptateurStrategique(BasePlugin):
    def __init__(self):
        super().__init__()
        self.nom = "plugin_adaptateur_strategique"
        self.description = "Filtre les plugins efficaces selon un seuil d’évaluation et propose une stratégie adaptative."
        self.seuil = 0.55  # Seuil minimal d'efficacité pour qu'un plugin soit retenu

    def tick(self, contexte: dict) -> dict:
        scores = contexte.get("plugin_scores", {})
        plugins_actifs = contexte.get("plugins_actifs", [])
        plugins_favoris = []

        for plugin, score in scores.items():
            if score >= self.seuil:
                plugins_favoris.append(plugin)

        # Fusion sans doublons
        plugins_suggérés = sorted(set(plugins_actifs + plugins_favoris))
        contexte["plugins_suggérés"] = plugins_suggérés

        log_msg = f"{self.nom} : plugins suggérés (≥ {self.seuil}) → {plugins_suggérés}"
        contexte.setdefault("plugins_log", []).append(log_msg)
        logger.info(f"[{self.nom}] Plugins suggérés : {plugins_suggérés}")

        return {
            "contexte": contexte,
            "meta": Meta(plugin=self.nom, info="Suggestions mises à jour en fonction des scores dynamiques.")
        }
