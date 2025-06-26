""" 
Plugin : auto_evaluation  
Rôle : Générer une auto-évaluation qualitative de la réponse produite  
Priorité : 7 (juste avant apprentissage & mémoire)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.auto_evaluation")

class AutoEvaluationPlugin(BasePlugin):
    meta = Meta(
        name="auto_evaluation",
        priority=7,
        version="1.1",  # mise à jour version
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("response", "")
        objectif = ctx.get("objectif", "Objectif inconnu")

        # Sécurité type
        if not isinstance(reponse, str):
            reponse = str(reponse)
        if not isinstance(objectif, str):
            objectif = str(objectif)

        reponse = reponse.strip()

        if not reponse:
            ctx["auto_evaluation"] = "❌ Échec : aucune réponse générée."
            plugins_log.append("AutoEvaluationPlugin : aucune réponse à évaluer.")
            logger.warning("[auto_evaluation] Pas de contenu pour évaluation.")
            return ctx

        # Critères simples (pour démarrer)
        longueur = len(reponse)
        evals = []

        if longueur < 30:
            evals.append("🔸 Réponse courte : peut manquer de profondeur.")
        elif longueur > 500:
            evals.append("✅ Réponse longue : potentiel de profondeur élevé.")
        else:
            evals.append("🟢 Réponse de longueur modérée.")

        r_lower = reponse.lower()
        if "je recommande" in r_lower:
            evals.append("🧠 Inclut un avis / conseil : bon signe de stratégie.")
        if "je ne sais pas" in r_lower:
            evals.append("⚠️ Incertitude détectée.")
        if objectif.lower() in r_lower:
            evals.append("🔍 L’objectif est bien traité dans la réponse.")
        else:
            evals.append("❓ Lien explicite à l’objectif non trouvé.")

        conclusion = "Auto-évaluation :\n" + "\n".join(evals)
        ctx["auto_evaluation"] = conclusion
        ctx["meta_reflexion"] = conclusion  # pour chaînage avec mémoire

        plugins_log.append("AutoEvaluationPlugin : évaluation générée.")
        logger.info(f"[auto_evaluation] {conclusion.replace(chr(10), ' / ')}")

        return ctx
