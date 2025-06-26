"""
Plugin : regulation_emotionnelle
Rôle : Réguler la tonalité émotionnelle des réponses (ex : neutre, chaleureux, assertif)
Priorité : 4.3 (après fusion ou génération brute)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.regulation_emotionnelle")

class RegulationEmotionnellePlugin(BasePlugin):
    meta = Meta(
        name="regulation_emotionnelle",
        priority=4.3,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        tonalite = ctx.get("emotional_tone", "neutre")  # personnalisable plus tard

        if not reponse:
            plugins_log.append("RegulationEmotionnellePlugin : aucune réponse à moduler.")
            return ctx

        # Transformation simple selon la tonalité
        if tonalite == "chaleureux":
            ctx["llm_response"] = f"🥰 Avec plaisir :\n{reponse}"
        elif tonalite == "assertif":
            ctx["llm_response"] = f"✅ Voici ce qu’il faut savoir :\n{reponse}"
        elif tonalite == "doux":
            ctx["llm_response"] = f"🌸 Si cela peut t’aider :\n{reponse}"
        elif tonalite == "neutre":
            ctx["llm_response"] = reponse.strip()
        else:
            ctx["llm_response"] = reponse  # fallback

        plugins_log.append(f"RegulationEmotionnellePlugin : tonalité appliquée → {tonalite}")
        logger.info(f"[regulation_emotionnelle] Tonalité : {tonalite}")

        return ctx
