""" 
Plugin : contestation  
Rôle : Remettre en question la réponse actuelle et proposer une alternative si pertinent  
Priorité : 7.8 (juste avant fin de cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.contestation")

class ContestationPlugin(BasePlugin):
    meta = Meta(
        name="contestation",
        priority=7.8,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("response", "").strip()

        if not reponse or len(reponse) < 20:
            plugins_log.append("ContestationPlugin : pas de réponse valable à contester.")
            return ctx

        # Simule une contestation intelligente
        critique = (
            "🧐 Auto-contestation :\n"
            "→ Cette réponse semble pertinente, mais peut-être trop générale.\n"
            "→ Elle pourrait omettre un contre-exemple, ou ignorer une alternative logique.\n"
            "→ Peut-être serait-il utile de reformuler pour un public non expert."
        )

        version2 = f"{reponse}\n\n📎 Révision suggérée :\nJe peux reformuler ou approfondir un angle si besoin."

        ctx["auto_contestation"] = critique
        ctx["response_v2"] = version2

        plugins_log.append("ContestationPlugin : réponse critiquée en interne.")
        logger.info("[contestation] Contestation interne générée.")

        return ctx
