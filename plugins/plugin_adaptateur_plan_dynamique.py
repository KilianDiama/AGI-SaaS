from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.adaptateur_plan")

class PluginAdaptateurPlanDynamique(BasePlugin):
    meta = Meta(
        name="plugin_adaptateur_plan_dynamique",
        version="1.0",
        priority=1.55,  # Juste après l’analyse de l’objectif
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip().lower()
        plan = ctx.get("plan", [])
        ancienne_intention = ctx.get("memoire_contextuelle", "").lower()
        intention_actuelle = ctx.get("message", "").lower()

        if not objectif or not intention_actuelle:
            ctx.setdefault("plugins_log", []).append("plugin_adaptateur_plan_dynamique : objectif ou intention manquant")
            return ctx

        if ancienne_intention and ancienne_intention != intention_actuelle:
            logger.info(f"[adaptation_plan] Changement détecté : {ancienne_intention} -> {intention_actuelle}")

            nouveau_plan = self.recalculer_plan(objectif, intention_actuelle)
            ctx["plan"] = nouveau_plan
            ctx["tache_courante"] = nouveau_plan[0]["étape"] if nouveau_plan else None

            ctx.setdefault("plugins_log", []).append("plugin_adaptateur_plan_dynamique : plan réajusté suite à changement d’intention")

        return ctx

    def recalculer_plan(self, objectif: str, intention: str):
        """Génère un plan simple basé sur une intention nouvelle."""
        steps = []

        if "analyse" in intention:
            steps = ["collecter infos", "résumer données", "identifier conclusions"]
        elif "résume" in intention:
            steps = ["identifier texte", "extraction points clés", "génération résumé"]
        elif "question" in intention:
            steps = ["comprendre question", "trouver infos", "formuler réponse"]
        else:
            steps = ["clarifier objectif", "proposer plan", "exécuter"]

        return [{"étape": e, "status": "à faire"} for e in steps]
