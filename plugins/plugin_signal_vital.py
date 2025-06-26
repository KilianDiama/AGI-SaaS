""" 
Plugin : signal_vital  
Rôle : Évaluer l'état cognitif général de l'AGI à chaque cycle (forme mentale)  
Priorité : 8.1 (après tous les autres)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.signal_vital")

class SignalVitalPlugin(BasePlugin):
    meta = Meta(
        name="signal_vital",
        priority=8.1,
        version="1.0",
        author="Matthieu & GPT"
    )

    MEMOIRE_PATH = "data/memoire_long_terme.json"

    def charger_memoire(self):
        if os.path.exists(self.MEMOIRE_PATH):
            try:
                with open(self.MEMOIRE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.get("plugins_log", [])
        memoire = self.charger_memoire()
        nb_plugins = len(plugins_log)
        nb_memoire = len(memoire)

        score = 50
        couleur = "🟡"

        if nb_plugins > 12:
            score += 20
        if nb_memoire > 50:
            score += 15
        if ctx.get("response") and "❌" not in ctx.get("response", ""):
            score += 10
        if "auto_contestation" in ctx and "⚠️" not in ctx["auto_contestation"]:
            score += 5

        score = min(score, 100)
        if score >= 90:
            couleur = "🟢"
        elif score < 60:
            couleur = "🔴"

        vital = f"{couleur} Signal vital cognitif : {score}/100"
        ctx["signal_vital"] = vital

        if not ctx.get("response"):
            ctx["response"] = vital

        plugins_log.append("SignalVitalPlugin : évaluation cognitive injectée.")
        logger.info("[signal_vital] Score vital calculé.")

        return ctx
