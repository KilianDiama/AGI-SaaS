from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.traceur_comportement")

class PluginTraceurComportement(BasePlugin):
    meta = Meta(
        name="plugin_traceur_comportement",
        version="1.0",
        priority=4.7,  # Juste avant la réponse finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        trace = ctx.setdefault("trace_comportement", [])
        now = datetime.utcnow().isoformat()

        checkpoints = [
            ("🧠 Intention", ctx.get("intention")),
            ("🎯 Objectif", ctx.get("objectif", {}).get("but")),
            ("🗺️ Plan", [e.get("étape") for e in ctx.get("plan", [])]),
            ("⚙️ Étape en cours", ctx.get("tache_courante")),
            ("🤖 LLM utilisé", f"{ctx.get('llm_backend')}/{ctx.get('llm_model')}"),
            ("📝 Prompt", ctx.get("llm_prompt")),
            ("📤 Réponse", ctx.get("response")),
            ("📈 Évaluation", ctx.get("evaluation_reponse", {}).get("note")),
        ]

        for label, valeur in checkpoints:
            if valeur:
                trace.append({
                    "timestamp": now,
                    "type": label,
                    "contenu": valeur
                })

        ctx["trace_comportement"] = trace
        ctx.setdefault("plugins_log", []).append("PluginTraceurComportement : trace comportement mise à jour.")
        logger.info("[traceur_comportement] Trace comportement enregistrée.")

        return ctx
