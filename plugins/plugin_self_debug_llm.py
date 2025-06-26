"""
Plugin : self_debug_llm
Rôle : Utiliser un LLM pour diagnostiquer une réponse jugée floue, incohérente ou incomplète
Priorité : 4.2 (juste après fusion, avant affichage final)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta
from utils.llm import call_llm  # Nécessite une fonction d'appel LLM existante

logger = logging.getLogger("plugin.self_debug_llm")

class SelfDebugLLMPlugin(BasePlugin):
    meta = Meta(
        name="self_debug_llm",
        priority=4.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    TRIGGERS = [
        "je ne suis pas sûr", "je ne sais pas", "cela dépend", "c’est difficile à dire", "peut-être"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        message = ctx.get("message", "")

        if not reponse or not message:
            plugins_log.append("SelfDebugLLMPlugin : données insuffisantes.")
            return ctx

        if any(t in reponse.lower() for t in self.TRIGGERS):
            prompt_debug = f"""Tu es un assistant expert en raisonnement logique. 
Une IA a donné cette réponse :\n\nQuestion : {message}\nRéponse : {reponse}\n\n
Analyse pourquoi la réponse est incertaine, propose une amélioration claire ou une reformulation."""

            try:
                suggestion = await call_llm(prompt_debug, model="mistral")  # Ou autre modèle local
                ctx["debug_llm_response"] = suggestion
                plugins_log.append("SelfDebugLLMPlugin : auto-diagnostic généré.")
                logger.info("[self_debug_llm] Suggestion de correction générée.")
            except Exception as e:
                logger.error(f"[self_debug_llm] Erreur LLM : {e}")
                plugins_log.append("SelfDebugLLMPlugin : erreur d'appel LLM pour debug.")

        return ctx
