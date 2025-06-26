# plugins/plugin_memoire_de_competence.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.memoire_de_competence")

class PluginMemoireDeCompetence(BasePlugin):
    meta = Meta(
        name="plugin_memoire_de_competence",
        priority=4.5,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_memoire_de_competence"

    async def run(self, ctx: Context) -> Context:
        reponses = ctx.get("reponses_curiosite", [])
        if not reponses:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucune réponse de curiosité disponible.")
            return ctx

        competences = ctx.setdefault("competences_mémorisées", {})

        ajoutées = 0
        for r in reponses:
            objet = r.get("objet")
            contenu = r.get("contenu")
            if objet and contenu:
                bloc = self._structurer_connaissance(objet, contenu)
                competences.setdefault(objet, []).append(bloc)
                ajoutées += 1

        logger.info(f"[{self.nom}] {ajoutées} compétences ajoutées")
        ctx.setdefault("plugins_log", []).append(f"{self.nom} : {ajoutées} blocs mémorisés")

        return ctx

    def _structurer_connaissance(self, objet: str, contenu: str) -> dict:
        return {
            "objet": objet,
            "connaissance": contenu.strip(),
            "timestamp": datetime.utcnow().isoformat()
        }
