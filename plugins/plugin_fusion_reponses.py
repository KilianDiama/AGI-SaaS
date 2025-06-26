# plugins/plugin_fusion_reponses.py

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.fusion")

class PluginFusionReponses(BasePlugin):
    meta = Meta(
        name="plugin_fusion_reponses",
        priority=4.2,  # Juste après vote
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        réponses = ctx.get("llm_responses", [])
        fusionnée = self.fusionner(réponses)
        ctx["response_logique"] = fusionnée
        ctx.setdefault("plugins_log", []).append("PluginFusionReponses : fusion réalisée.")
        logger.info(f"[fusion] Réponse fusionnée :\n{fusionnée[:200]}...")
        return ctx

    def fusionner(self, réponses: list[str]) -> str:
        if not réponses:
            return "Je n'ai pas de réponse pour l'instant."

        # Nettoyage des modèles
        textes = [re.sub(r"\[.*?\]", "", r).strip() for r in réponses if r.strip()]
        textes = list(dict.fromkeys(textes))  # Suppression doublons exacts

        if len(textes) == 1:
            return textes[0]

        # Fusion simple pour commencer
        fusion = " ".join(textes)
        fusion = re.sub(r"\s+", " ", fusion).strip()

        # Bonus : si trop long, couper intelligemment
        if len(fusion) > 1000:
            fusion = fusion[:1000].rsplit(".", 1)[0] + "."

        return fusion
