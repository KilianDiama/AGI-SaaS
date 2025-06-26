# plugins/plugin_agent_cognitif.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.agent_cognitif")

class PluginAgentCognitif(BasePlugin):
    meta = Meta(
        name="plugin_agent_cognitif",
        priority=3.2,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.memoire_interne = []

    async def run(self, ctx: Context) -> Context:
        cycle_id = ctx.get("cycle_id")
        objectif = ctx.get("objectif", {}).get("but", "")
        reponse = ctx.get("llm_response", "").strip()
        erreur = ctx.get("error", {})
        note = ctx.get("evaluation_reponse", {}).get("note", 0)

        # ⏺️ Trace cognitive
        trace = {
            "timestamp": datetime.utcnow().isoformat(),
            "cycle_id": cycle_id,
            "objectif": objectif,
            "reponse": reponse[:150],
            "erreur": erreur.get("message", None),
            "note": note,
        }
        self.memoire_interne.append(trace)

        # ⚠️ Détection de réponse faible
        if note < 2 and not erreur.get("message") and len(reponse) < 10:
            suggestion = f"🔁 Reformule la dernière action pour clarifier ou améliorer la réponse. Objectif : {objectif}"
            ctx["demande_llm"] = suggestion
            ctx.setdefault("plugins_log", []).append(f"PluginAgentCognitif : faible réponse détectée → ajustement déclenché")
            logger.warning(f"[Agent Cognitif] Suggestion d’ajustement envoyée : {suggestion}")

        return ctx
