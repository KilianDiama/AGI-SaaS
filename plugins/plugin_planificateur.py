from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.planificateur")

class PluginPlanificateur(BasePlugin):
    meta = Meta(
        name="plugin_planificateur",
        version="1.2",
        priority=2.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "")
        if not objectif:
            logger.debug("[planificateur] Aucun objectif détecté.")
            return ctx

        # Analyse naïve (peut être boostée via LLM plus tard)
        plan = self._générer_plan(objectif)
        if not plan:
            logger.info("[planificateur] Aucun plan généré.")
            return ctx

        ctx["plan"] = plan
        ctx.setdefault("plugins_log", []).append("PluginPlanificateur : plan généré.")
        logger.info(f"[planificateur] Plan généré pour : {objectif}")
        return ctx

    def _générer_plan(self, objectif: str):
        objectif = objectif.lower()

        if "plugin" in objectif:
            return [
                {"étape": "identifier le besoin", "status": "à faire"},
                {"étape": "rédiger le squelette du plugin", "status": "à faire"},
                {"étape": "implémenter la logique", "status": "à faire"},
                {"étape": "tester en local", "status": "à faire"},
                {"étape": "valider l'intégration", "status": "à faire"},
            ]
        elif "assistant" in objectif or "ia" in objectif:
            return [
                {"étape": "analyser le besoin de l'utilisateur", "status": "à faire"},
                {"étape": "définir les modules nécessaires", "status": "à faire"},
                {"étape": "composer l’architecture des plugins", "status": "à faire"},
                {"étape": "implémenter les briques de base", "status": "à faire"},
                {"étape": "tester en boucle fermée", "status": "à faire"},
            ]
        else:
            return [
                {"étape": "analyser l’objectif", "status": "à faire"},
                {"étape": "identifier les actions clés", "status": "à faire"},
                {"étape": "structurer les étapes logiques", "status": "à faire"},
                {"étape": "préparer les conditions de réussite", "status": "à faire"},
            ]
