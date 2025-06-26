"""
Plugin : veille_interne
Rôle : Observer le flux de pensée et détecter les désalignements cognitifs ou affectifs
Priorité : 15
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.veille_interne")

class VeilleInternePlugin(BasePlugin):
    meta = Meta(
        name="veille_interne",
        priority=15,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        pensée = ctx.get("llm_response", "")
        état = ctx.get("état_interieur", {})

        signal = {
            "désalignement_detecté": False,
            "type": None,
            "indice": 0
        }

        # Analyse simple pour détecter signes de tension
        tensions = ["je doute", "je ne suis pas sûre", "je me contredis", "je suis divisée", "confus", "paradoxe"]
        score = sum(1 for t in tensions if t in pensée.lower())

        if score > 0:
            signal["désalignement_detecté"] = True
            signal["type"] = "tension_interne"
            signal["indice"] = score

            logger.warning(f"[veille_interne] Désalignement détecté : {score}")
            plugins_log.append(f"VeilleInternePlugin : ⚠️ désalignement cognitif ({score})")
        else:
            logger.info("[veille_interne] Aucun désalignement détecté")
            plugins_log.append("VeilleInternePlugin : ✅ stabilité cognitive")

        ctx["veille_interne_signal"] = signal
        return ctx
