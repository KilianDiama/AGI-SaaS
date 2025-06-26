import logging
from noyau_core import BasePlugin, Context, Meta
from difflib import SequenceMatcher

logger = logging.getLogger("plugin.alignment_checker")

class PluginAlignmentChecker(BasePlugin):
    meta = Meta(
        name="plugin_alignment_checker",
        version="1.0",
        priority=4.6,  # Après évaluation, avant réponse finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "").lower().strip()
        objectif = ctx.get("objectif", {}).get("but", "").lower().strip()
        response = ctx.get("response", "").lower().strip()

        plugins_log = ctx.setdefault("plugins_log", [])

        if not intention or not response:
            ctx["alignment_score"] = 0.0
            plugins_log.append("plugin_alignment_checker : données manquantes, score 0.0")
            return ctx

        # On fusionne intention et objectif pour une comparaison plus riche
        cible = f"{intention} {objectif}".strip()

        score = SequenceMatcher(None, cible, response).ratio()
        score_100 = round(score * 100, 2)

        ctx["alignment_score"] = score_100
        plugins_log.append(f"plugin_alignment_checker : score d'alignement = {score_100}%")
        logger.info(f"[alignment] Alignement intention↔réponse : {score_100}%")

        return ctx
