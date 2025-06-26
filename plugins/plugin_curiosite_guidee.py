# plugins/plugin_curiosite_guidee.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.curiosite_guidee")

class PluginCuriositeGuidee(BasePlugin):
    meta = Meta(
        name="plugin_curiosite_guidee",
        priority=4.2,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_curiosite_guidee"
        self.seuil_curiosite = 1  # objets rarement vus → déclenche curiosité

    async def run(self, ctx: Context) -> Context:
        objets = ctx.get("objets_connaissance", {})
        if not objets:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun objet enregistré.")
            return ctx

        questions = []
        for nom, données in objets.items():
            if données.get("comptage", 0) <= self.seuil_curiosite:
                questions.append(self._générer_question(nom))

        if questions:
            ctx.setdefault("questions_curiosite", []).extend(questions)
            logger.info(f"[{self.nom}] Questions générées : {questions}")
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : {len(questions)} questions créées")
        else:
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucun objet peu fréquent détecté")

        return ctx

    def _générer_question(self, objet: str) -> str:
        return f"🧠 Qu’est-ce que « {objet} » et comment cela fonctionne-t-il dans ce contexte ?"
