"""
Plugin : observateur_silencieux
Rôle : Enregistrer passivement les désalignements, tensions ou conflits internes détectés
Priorité : 32
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime
import logging

logger = logging.getLogger("plugin.observateur_silencieux")

class ObservateurSilencieuxPlugin(BasePlugin):
    meta = Meta(
        name="observateur_silencieux",
        priority=32,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        journal = ctx.setdefault("journal_interne", [])
        plugins_log = ctx.setdefault("plugins_log", [])

        signal = ctx.get("veille_interne_signal", {})
        score = ctx.get("coherence_score", 100)
        alertes = ctx.get("coherence_alertes", [])

        if signal.get("désalignement_detecté") or score < 85:
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "désalignement": signal,
                "coherence_score": score,
                "alertes": alertes,
                "extrait_conscience": ctx.get("llm_response", "")
            }

            journal.append(log)
            logger.info("[observateur_silencieux] Trace ajoutée au journal interne")
            plugins_log.append("ObservateurSilencieuxPlugin : journal mis à jour")

        else:
            plugins_log.append("ObservateurSilencieuxPlugin : pas d’entrée (état stable)")
            logger.debug("[observateur_silencieux] Rien à signaler")

        ctx["journal_interne"] = journal
        return ctx
