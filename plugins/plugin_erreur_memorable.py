"""
Plugin : erreur_memorable
Rôle : Stocker de façon structurée les erreurs rencontrées pour éviter les répétitions
Priorité : 2.4 (après logs et avant génération)
Auteur : AGI & Matthieu
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.erreur_memorable")

class ErreurMemorablePlugin(BasePlugin):
    meta = Meta(
        name="erreur_memorable",
        priority=2.4,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        erreurs = ctx.setdefault("erreurs_memorisees", [])

        last_logs = ctx.get("plugins_log", [])[-5:]
        anomalies = [l for l in last_logs if "erreur" in l.lower() or "échec" in l.lower() or "fallback" in l.lower()]

        for anomalie in anomalies:
            erreurs.append({
                "timestamp": datetime.utcnow().isoformat(),
                "type": "anomalie_cycle",
                "contenu": anomalie
            })

        if anomalies:
            plugins_log.append(f"ErreurMemorablePlugin : {len(anomalie)} erreur(s) mémorisée(s)")
            logger.warning("[erreur_memorable] Anomalies capturées et stockées.")
        else:
            plugins_log.append("ErreurMemorablePlugin : aucun échec à mémoriser.")

        return ctx
