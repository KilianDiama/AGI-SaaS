"""
Plugin : indexeur_connaissances
Rôle : Structurer et sauvegarder les connaissances acquises de manière consultable (index mémoire)
Priorité : 4.0 (après génération ou décision)
Auteur : AGI & Matthieu
"""

import logging
import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.indexeur_connaissances")

class IndexeurConnaissancesPlugin(BasePlugin):
    meta = Meta(
        name="indexeur_connaissances",
        priority=4.0,
        version="1.0",
        author="AGI & Matthieu"
    )

    INDEX_PATH = "index_connaissances.json"

    def charger_index(self):
        if os.path.exists(self.INDEX_PATH):
            with open(self.INDEX_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def enregistrer_index(self, index):
        with open(self.INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        index = self.charger_index()

        concepts = ctx.get("concepts_memorises", [])
        nouveau = []

        for concept in concepts:
            item = {
                "concept": concept,
                "date": datetime.utcnow().isoformat(),
                "tag": ctx.get("objectif_externe", "général")
            }
            if item not in index:
                nouveau.append(item)
                index.append(item)

        if nouveau:
            self.enregistrer_index(index)
            plugins_log.append(f"IndexeurConnaissancesPlugin : {len(nouveau)} concept(s) indexé(s)")
            logger.info(f"[indexeur_connaissances] {len(nouveau)} nouveau(x) concept(s) enregistré(s)")

        return ctx
