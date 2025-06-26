""" 
Plugin : perception_externe  
Rôle : Lire une perception textuelle externe pour la rendre disponible dans le contexte cognitif  
Priorité : 2 (juste après autonomie)  
Auteur : Matthieu & GPT  
"""

import logging
import os
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.perception_externe")

class PerceptionExternePlugin(BasePlugin):
    meta = Meta(
        name="perception_externe",
        priority=2,
        version="1.0",
        author="Matthieu & GPT"
    )

    PERCEPTION_PATH = "data/perception.txt"

    def lire_perception(self):
        if os.path.exists(self.PERCEPTION_PATH):
            try:
                with open(self.PERCEPTION_PATH, "r", encoding="utf-8") as f:
                    contenu = f.read().strip()
                    return contenu
            except Exception as e:
                logger.warning(f"[perception_externe] Erreur de lecture : {e}")
        return ""

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        perception = self.lire_perception()
        if perception:
            ctx["perception_externe"] = perception
            plugins_log.append("PerceptionExternePlugin : perception externe détectée et injectée.")
            logger.info(f"[perception_externe] Perception chargée : {perception[:80]}...")
        else:
            plugins_log.append("PerceptionExternePlugin : aucune perception détectée.")
            logger.info("[perception_externe] Aucune donnée perçue.")

        return ctx
