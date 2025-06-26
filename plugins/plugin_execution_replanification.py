# plugins/plugin_execution_replanification.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.execution_replanification")

class PluginExecutionReplanification(BasePlugin):
    meta = Meta(
        name="plugin_execution_replanification",
        version="1.0",
        author="Toi & GPT",
        priority=3.4
    )

    def __init__(self):
        self.nom = "plugin_execution_replanification"

    async def run(self, ctx: Context) -> Context:
        if not ctx.get("relancer_plan"):
            ctx.setdefault("plugins_log", []).append(f"{self.nom} : aucune replanification requise.")
            return ctx

        objectif = ctx.get("objectif", {}).get("but", "objectif inconnu")
        nouveau_plan = self._generer_nouveau_plan(objectif)

        ctx["plan_generé"] = nouveau_plan
        ctx["etat_execution"] = "plan_relancé"
        ctx["etape_actuelle"] = 0
        if nouveau_plan:
            ctx["étape_en_cours"] = nouveau_plan[0]
        else:
            ctx["étape_en_cours"] = "aucune étape définie"

        ctx.setdefault("plugins_log", []).append(
            f"{self.nom} : 🔄 Plan relancé pour l’objectif « {objectif} » ({len(nouveau_plan)} étapes)."
        )
        return ctx

    def _generer_nouveau_plan(self, objectif: str) -> list:
        return [
            f"Analyser à nouveau l’objectif : {objectif}",
            "Identifier les échecs précédents",
            "Formuler un nouveau plan d’action",
            "Vérifier la cohérence du plan avant exécution"
        ]
