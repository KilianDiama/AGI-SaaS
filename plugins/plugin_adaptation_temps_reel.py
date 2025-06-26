"""
Plugin : adaptation_temps_reel
Rôle : Ajuster dynamiquement le comportement cognitif selon des signaux internes (ex : surcharge, tonalité)
Priorité : 2.3 (juste avant exécution LLM)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.adaptation_temps_reel")

class AdaptationTempsReelPlugin(BasePlugin):
    meta = Meta(
        name="adaptation_temps_reel",
        priority=2.3,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        tonalite = ctx.get("tonalite_utilisateur", "neutre")
        surcharge_detectee = ctx.get("surcharge_cognitive", False)
        cyclique_detecte = ctx.get("alerte_coherence", "")
        debug_auto = ctx.get("debug_llm_response", "")

        mode_adaptatif = "standard"

        if surcharge_detectee:
            mode_adaptatif = "réduction_cognitive"
        elif tonalite == "urgent":
            mode_adaptatif = "réponse_directe"
        elif debug_auto:
            mode_adaptatif = "auto_correction_active"
        elif cyclique_detecte:
            mode_adaptatif = "vérification_cohérence"

        ctx["mode_adaptatif"] = mode_adaptatif
        plugins_log.append(f"AdaptationTempsReelPlugin : mode actif → {mode_adaptatif}")
        logger.info(f"[adaptation_temps_reel] Mode cognitif ajusté à : {mode_adaptatif}")

        return ctx
