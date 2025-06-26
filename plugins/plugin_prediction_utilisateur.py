""" 
Plugin : prediction_utilisateur  
Rôle : Prédire la prochaine intention ou question probable de l'utilisateur  
Priorité : 7.2 (après synthèse, juste avant auto-évaluation)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.prediction_utilisateur")

class PredictionUtilisateurPlugin(BasePlugin):
    meta = Meta(
        name="prediction_utilisateur",
        priority=7.2,
        version="1.1",  # ← version corrigée
        author="Matthieu & GPT"
    )

    def nettoyer(self, val) -> str:
        """Convertit proprement n'importe quelle entrée en string minuscule."""
        if isinstance(val, dict):
            val = val.get("but", "")  # ou autre champ pertinent
        return str(val).strip().lower()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif = self.nettoyer(ctx.get("objectif", ""))
        reponse = self.nettoyer(ctx.get("response", ""))

        if not objectif and not reponse:
            plugins_log.append("PredictionUtilisateurPlugin : pas d'entrée à analyser.")
            return ctx

        suggestions = [
            "demander un plan d'exécution détaillé",
            "demander une amélioration ou une reformulation",
            "provoquer un débat ou dialogue interne",
            "créer une version SaaS ou API du concept",
            "demander un résumé ou une synthèse globale",
            "suggérer un test en condition réelle",
            "envoyer la réponse à un humain pour validation"
        ]
        prediction = random.choice(suggestions)

        ctx["prediction_utilisateur"] = f"📍 Intention probable de l'utilisateur : {prediction}"
        plugins_log.append("PredictionUtilisateurPlugin : intention anticipée.")
        logger.info(f"[prediction_utilisateur] → {prediction}")

        return ctx
