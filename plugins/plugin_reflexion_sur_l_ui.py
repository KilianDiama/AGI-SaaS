# plugins/plugin_reflexion_sur_l_ui.py

"""
Plugin : reflexion_sur_l_ui
Rôle   : Analyse la qualité de l’interaction avec l’utilisateur et propose des adaptations de style ou de clarification
Priorité : -15 (début de cycle)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reflexion_sur_l_ui")

class ReflexionSurUIPlugin(BasePlugin):
    meta = Meta(
        name="reflexion_sur_l_ui",
        priority=-15,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        longueur = len(message)
        suggestions = []

        if longueur < 10:
            suggestions.append("La demande est très courte — proposer clarification ?")
        elif longueur > 300:
            suggestions.append("Demande très longue — résumer ou découper la tâche ?")

        # Détection de style ou ton
        if any(m in message.lower() for m in ["hein", "wsh", "bb", "gros", "frère"]):
            suggestions.append("Langage familier détecté — adapter ton ou formalisme ?")
        elif any(m in message.lower() for m in ["merci", "s'il te plaît", "je voudrais"]):
            suggestions.append("Tonalité polie — style coopératif activé")

        # Détection d’ambiguïté
        if "ça" in message.lower() or "fais le" in message.lower():
            suggestions.append("Référence floue ('ça') détectée — suggérer reformulation ?")

        ctx["reflexion_ui"] = suggestions
        log.append(f"ReflexionSurUIPlugin : {len(suggestions)} remarques sur l’interaction utilisateur.")
        logger.info(f"[reflexion_ui] Suggestions d’interaction : {suggestions}")

        return ctx
