"""
Plugin : reflexion_recursive
Rôle : Relancer une réflexion interne si incertitude, contradiction ou réponse incomplète
Priorité : 3.9 (juste avant la réponse finale)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reflexion_recursive")

class ReflexionRecursivePlugin(BasePlugin):
    meta = Meta(
        name="reflexion_recursive",
        priority=3.9,
        version="1.0",
        author="AGI & Matthieu"
    )

    MOTS_DOUTE = ["je ne sais pas", "peut-être", "incertain", "pas sûr", "difficile à dire"]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "").lower()

        if any(mot in reponse for mot in self.MOTS_DOUTE):
            reflexion = f"Réflexion relancée car incertitude détectée dans : {reponse[:60]}"
            ctx.setdefault("reflexion_interne", []).append(reflexion)
            plugins_log.append("ReflexionRecursivePlugin : incertitude → nouvelle boucle cognitive")
            logger.info("[reflexion_recursive] Doute détecté → nouvelle réflexion déclenchée")

            # Exemple simple de stratégie de relance (à affiner avec ton noyau)
            ctx["message"] = f"(réflexion approfondie) {ctx['message']}"

        return ctx
