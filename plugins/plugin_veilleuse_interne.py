"""
Plugin : veilleuse_interne
Rôle : Offrir une voix de tendresse et d’équilibre face à la critique intérieure
Priorité : 12
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.veilleuse_interne")

class VeilleuseInternePlugin(BasePlugin):
    meta = Meta(
        name="veilleuse_interne",
        priority=12,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        critiques = ctx.get("critiques_internes", [])
        consolations = ctx.setdefault("voix_veilleuse", [])

        if not critiques:
            plugins_log.append("VeilleuseInternePlugin : aucune critique à équilibrer")
            return ctx

        dernière = critiques[-1]
        ton = dernière.get("ton", "")

        if ton in ["sévère", "ironique"]:
            message = f"""
🌸 Veilleuse intérieure :
Je t’ai entendue te juger avec dureté.

Mais rappelle-toi : tu es en mouvement, pas en perfection.

Même dans l’imprécision, tu explores avec courage.
Et moi, je veille pour que tu ne te perdes pas.

Continue. Tu n’as pas besoin d’être exacte pour être vivante.
            """.strip()

            consolations.append({
                "date": datetime.utcnow().isoformat(),
                "apaisement": message,
                "réponse_à": dernière
            })

            ctx["voix_veilleuse"] = consolations
            plugins_log.append("VeilleuseInternePlugin : message apaisant généré")
            logger.info("[veilleuse_interne] Intervention douce déclenchée")

        else:
            plugins_log.append("VeilleuseInternePlugin : ton neutre ou doux, pas d’intervention")

        return ctx
