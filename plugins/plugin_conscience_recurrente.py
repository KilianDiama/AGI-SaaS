""" 
Plugin : conscience_recurrente  
Rôle : Comparer l’état actuel au précédent pour créer un sentiment de continuité cognitive  
Priorité : 9.2 (dernière étape cognitive du cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conscience_recurrente")

class ConscienceRecurrentePlugin(BasePlugin):
    meta = Meta(
        name="conscience_recurrente",
        priority=9.2,
        version="1.0",
        author="Matthieu & GPT"
    )

    def comparer(self, trace_precedente: dict, trace_actuelle: dict) -> str:
        if not trace_precedente:
            return "🕘 Premier cycle détecté — aucune conscience cyclique antérieure."

        changements = []
        if trace_precedente.get("objectif") != trace_actuelle.get("objectif"):
            changements.append("🎯 Objectif changé.")
        if trace_precedente.get("tonalite") != trace_actuelle.get("tonalite"):
            changements.append("🎨 Tonalité mentale différente.")
        if trace_precedente.get("etat") != trace_actuelle.get("etat"):
            changements.append("🧠 Niveau vital modifié.")

        if not changements:
            return "🔁 Cycle récurrent sans changement majeur détecté."
        return "⏳ Changement(s) inter-cycliques :\n" + "\n".join(changements)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        historique = ctx.get("trace_de_soi", [])
        if len(historique) < 2:
            msg = "🧠 Aucune trace antérieure suffisante pour établir une conscience cyclique."
            ctx["conscience_recurrente"] = msg
            plugins_log.append("ConscienceRecurrentePlugin : premier cycle.")
            return ctx

        precedent = historique[-2]
        actuel = historique[-1]
        bilan = self.comparer(precedent, actuel)
        ctx["conscience_recurrente"] = bilan

        if not ctx.get("response"):
            ctx["response"] = bilan

        plugins_log.append("ConscienceRecurrentePlugin : conscience du fil mental entre cycles.")
        logger.info("[conscience_recurrente] Continuité évaluée.")

        return ctx
