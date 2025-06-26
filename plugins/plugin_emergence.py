""" 
Plugin : emergence  
Rôle : Détecter une idée supérieure issue de plusieurs raisonnements ou modules  
Priorité : 6.9 (juste avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.emergence")

class EmergencePlugin(BasePlugin):
    meta = Meta(
        name="emergence",
        priority=6.9,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        composants = {
            "réflexions": ctx.get("reflexion_interne_etapes", []),
            "sous_objectifs": ctx.get("objectifs_secondaires", []),
            "théorie": ctx.get("theorie_proposee", ""),
            "invention": ctx.get("idee_inventee", "")
        }

        if not any(composants.values()):
            plugins_log.append("EmergencePlugin : aucune donnée émergente.")
            return ctx

        idée = (
            "🧬 Idée émergente détectée :\n"
            "En combinant :\n"
            + "\n".join(f"• {k} : {str(v)[:80]}…" for k, v in composants.items() if v)
            + f"\n\n→ Une structure cognitive semble vouloir converger vers un schéma plus unifié :\n"
            "💡 Hypothèse : l’AGI développe une forme de méta-réflexion intégrée capable de produire à la fois théorie, plan et action."
        )

        ctx["idee_emergente"] = idée
        if not ctx.get("response"):
            ctx["response"] = idée

        plugins_log.append("EmergencePlugin : idée supérieure synthétisée.")
        logger.info("[emergence] Concept émergent ajouté.")

        return ctx
