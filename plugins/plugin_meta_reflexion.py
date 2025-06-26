# plugins/plugin_meta_reflexion.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.meta_reflexion")

class PluginMetaReflexion(BasePlugin):
    meta = Meta(
        name="plugin_meta_reflexion",
        version="1.1",  # ← version corrigée
        author="Toi & GPT",
        priority=3.6
    )

    def __init__(self):
        self.nom = "plugin_meta_reflexion"

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("historique_execution", [])
        log = ctx.setdefault("plugins_log", [])

        # Vérification du type de l’historique
        if not isinstance(historique, list):
            log.append(f"{self.nom} : format invalide pour historique_execution.")
            ctx["meta_reflexion"] = "⚠️ Historique d'exécution illisible ou corrompu."
            return ctx

        # Extraction des erreurs
        erreurs = [
            e for e in historique
            if isinstance(e, dict) and e.get("status") == "échec"
        ]

        reflexions = []
        for erreur in erreurs:
            cause = str(erreur.get("cause", "non spécifiée"))
            etape = str(erreur.get("étape", "inconnue"))
            reflexions.append(f"🧠 Échec détecté à l’étape « {etape} ». Cause probable : {cause}.")

        # Injection dans le contexte
        if reflexions:
            ctx["meta_reflexion"] = "\n".join(reflexions)
            log.append(f"{self.nom} : réflexions générées ({len(reflexions)}).")
        else:
            ctx["meta_reflexion"] = "✅ Aucun échec détecté récemment."
            log.append(f"{self.nom} : rien à signaler.")

        return ctx
