from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.self_adjust")

class PluginSelfAdjustCalibrator(BasePlugin):
    meta = Meta(
        name="plugin_self_adjust_calibrator",
        version="1.0",
        priority=2.9,  # Juste avant le choix de LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        evaluation = ctx.get("evaluation_reponse", {})
        note = evaluation.get("note", 0)
        erreurs = ctx.get("errors", [])
        historique = ctx.get("history", [])
        longueur = evaluation.get("longueur", 0)

        ajustements = []

        # Ajustement du ton ou style
        if note <= 2:
            ajustements.append("🔧 Note basse : simplifier les réponses et réduire la longueur.")
            ctx["style_instruction"] = "Style simplifié, ton amical, phrases plus courtes."

        # Ajustement de la mémoire si trop d’erreurs
        if len(erreurs) >= 3:
            ajustements.append("🧠 Plusieurs erreurs : réduire l’usage mémoire ou désactiver des modules à risque.")
            ctx["memoire_contextuelle_activee"] = False

        # Réaction à l’inaction ou à la boucle
        if len(historique) >= 5 and all("je vais faire de mon mieux" in msg["message"].lower() for msg in historique[-3:]):
            ajustements.append("🔁 Comportement en boucle détecté : injection d'un objectif d'exploration.")
            ctx["objectif"]["but"] = "explorer des stratégies de réponse variées"

        # Enregistrement
        ctx["ajustements_dynamiques"] = ajustements
        ctx.setdefault("plugins_log", []).append("plugin_self_adjust_calibrator : ajustements appliqués.")
        logger.info(f"[calibrator] Ajustements détectés : {ajustements}")

        return ctx
