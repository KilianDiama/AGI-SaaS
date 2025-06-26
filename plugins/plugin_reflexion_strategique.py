# plugins/plugin_reflexion_strategique.py

import random
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.reflexion_strategique")

class PluginReflexionStrategique(BasePlugin):
    meta = Meta(
        name="plugin_reflexion_strategique",
        version="1.0",
        priority=2.8,
        author="Toi & GPT"
    )

    def __init__(self, plugin_objectifs=None):
        super().__init__()
        self.plugin_objectifs = plugin_objectifs

    async def run(self, ctx: Context) -> Context:
        if not self.plugin_objectifs:
            ctx.setdefault("plugins_log", []).append("PluginReflexionStrategique : aucun plugin_objectifs fourni")
            return ctx

        diagnostic = self.analyser_etat()
        orientation = self.proposer_orientation()

        ctx["reflexion_strategique"] = {
            "diagnostic": diagnostic,
            "orientation": orientation
        }

        ctx.setdefault("plugins_log", []).append("PluginReflexionStrategique : réflexion stratégique injectée.")
        logger.info(f"[ReflexionStrategique] Diagnostic : {diagnostic}")
        logger.info(f"[ReflexionStrategique] Orientation : {orientation}")
        return ctx

    def analyser_etat(self):
        etat = self.plugin_objectifs.état_global()
        return {
            "diagnostic": f"Objectifs en cours : {etat.get('en cours', 0)}, à faire : {etat.get('à faire', 0)}, terminés : {etat.get('terminé', 0)}",
            "timestamp": datetime.utcnow().isoformat()
        }

    def proposer_orientation(self):
        id_obj, data = self.plugin_objectifs.obtenir_prochain_objectif()
        if not data:
            return {
                "type": "attente",
                "message": "Aucun objectif en cours. En attente de nouvelles instructions.",
                "timestamp": datetime.utcnow().isoformat()
            }

        orientation = random.choice([
            "Continuer selon le plan.",
            "Reformuler l'objectif pour le simplifier.",
            "Créer un objectif secondaire pour décomposer le travail.",
            "Changer la priorité vers un objectif plus critique.",
            "Suspendre l’objectif en cours : manque de contexte ou de données."
        ])

        return {
            "type": "stratégie",
            "objectif_id": id_obj,
            "objectif": data.get("objectif", "non défini"),
            "orientation": orientation,
            "timestamp": datetime.utcnow().isoformat()
        }
