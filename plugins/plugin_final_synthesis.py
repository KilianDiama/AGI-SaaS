# plugins/plugin_final_synthesis.py

"""
Plugin : final_synthesis
Rôle   : Combine toutes les versions générées pour créer une réponse finale optimisée
Priorité : 99 (juste avant le rendu utilisateur)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.final_synthesis")

class FinalSynthesisPlugin(BasePlugin):
    meta = Meta(
        name="final_synthesis",
        priority=99,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        base = ctx.get("llm_response", "")
        rev = ctx.get("llm_response_revised", "")
        meta = ctx.get("meta_choix_final", "")
        contre = ctx.get("contre_arguments", [])
        concepts = ctx.get("emergence_logique", [])

        synthese = "🧠 **Synthèse cognitive finale**\n\n"

        if meta:
            synthese += f"Version sélectionnée :\n{meta}\n\n"
        elif rev:
            synthese += f"Révision basée sur objections :\n{rev}\n\n"
        elif base:
            synthese += f"Réponse brute :\n{base}\n\n"
        else:
            synthese += "Aucune réponse générée.\n"

        if contre:
            synthese += f"⚖️ Objections internes considérées :\n- " + "\n- ".join(contre) + "\n\n"

        if concepts:
            synthese += f"🔍 Concepts logiques détectés :\n- " + "\n- ".join(concepts) + "\n\n"

        synthese += "✅ Réponse stabilisée après introspection multi-niveaux."

        ctx["reponse_finale"] = synthese
        log.append("FinalSynthesisPlugin : réponse finale générée.")
        logger.info("[final_synthesis] Synthèse générée et injectée.")

        return ctx
