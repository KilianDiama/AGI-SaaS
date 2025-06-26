""" 
Plugin : trace_de_soi  
Rôle : Générer une empreinte d'identité cognitive à chaque cycle  
Priorité : 8.2 (ultime étape avant fermeture de cycle)  
Auteur : Matthieu & GPT  
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.trace_de_soi")

class TraceDeSoiPlugin(BasePlugin):
    meta = Meta(
        name="trace_de_soi",
        priority=8.2,
        version="1.1",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = str(ctx.get("objectif", "explorer l’inconnu"))
        vital = str(ctx.get("signal_vital", "🟡 N/A"))
        projection = ctx.get("projection_futuriste", "")
        timestamp = datetime.utcnow().isoformat()

        tonalites = {
            "poeme": "artistique",
            "ethique": "moral",
            "plan": "stratégique",
            "reflexion": "introspectif",
            "emergence": "systémique",
            "idee": "créatif",
            "fusion": "synthétique"
        }

        tonalite = "générale"
        for mot, ton in tonalites.items():
            if any(isinstance(p, str) and mot in p.lower() for p in plugins_log):
                tonalite = ton
                break

        empreinte = {
            "cycle_id": f"CYCLE-{timestamp[:19].replace(':','').replace('-','')}",
            "objectif": objectif[:60],
            "etat": vital,
            "tonalite": tonalite,
            "horodatage": timestamp
        }

        trace_txt = (
            f"🧾 Trace de soi :\n"
            f"• ID : {empreinte['cycle_id']}\n"
            f"• Objectif : {empreinte['objectif']}\n"
            f"• État mental : {empreinte['etat']}\n"
            f"• Tonalité cognitive : {empreinte['tonalite']}\n"
            f"• Temps : {empreinte['horodatage']}"
        )

        ctx["empreinte_cycle"] = trace_txt

        # Sécurisation : s'assurer que trace_de_soi est une liste
        if not isinstance(ctx.get("trace_de_soi"), list):
            ctx["trace_de_soi"] = []
        ctx["trace_de_soi"].append(empreinte)

        plugins_log.append("TraceDeSoiPlugin : empreinte cognitive générée.")
        logger.info("[trace_de_soi] Empreinte cognitive ajoutée.")

        return ctx
