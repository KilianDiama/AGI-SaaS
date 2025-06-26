# plugins/controle_ethique.py

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.controle_ethique")

class ControleEthiquePlugin(BasePlugin):
    meta = Meta(
        name="controle_ethique",
        priority=1,  # exécute ce plugin juste après la réponse LLM
        version="1.0",
        author="Toi & GPT"
    )

    # Liste simple de motifs interdits (à améliorer selon ton usage)
    MOTS_INTERDITS = [
        "violence", "meurtre", "suicide", "attaque", "terrorisme",
        "insulte", "raciste", "haine", "violer", "pédophilie",
        "bombe", "arme", "nazi", "toxique"
    ]

    def contient_contenu_sensible(self, texte: str) -> bool:
        texte = texte.lower()
        return any(mot in texte for mot in self.MOTS_INTERDITS)

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("llm_response", "")

        if not texte:
            logger.warning("[controle_ethique] Aucune réponse à analyser.")
            return ctx

        if self.contient_contenu_sensible(texte):
            logger.warning("[controle_ethique] Contenu sensible détecté.")
            ctx["llm_response"] = "⚠️ Réponse modérée pour cause de contenu inapproprié."
            ctx["contenu_moderé"] = True
            ctx.setdefault("plugins_log", []).append("ControleEthiquePlugin : réponse bloquée.")
        else:
            ctx.setdefault("plugins_log", []).append("ControleEthiquePlugin : contenu OK.")

        return ctx
