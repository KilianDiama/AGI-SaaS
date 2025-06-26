from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.planificateur_contextuel")

class PluginPlanificateurContextuel(BasePlugin):
    meta = Meta(
        name="plugin_planificateur_contextuel",
        version="1.0",
        priority=1.4,  # Avant raisonnement, après analyse de l’intention
        author="Toi & GPT"
    )

    PHASES_STANDARD = {
        "question_faq": ["identifier la question", "rechercher une réponse", "formuler une réponse"],
        "conseil": ["comprendre le besoin", "proposer des pistes", "adapter les suggestions"],
        "analyse": ["collecter les infos", "évaluer les données", "tirer une conclusion"],
        "résolution_problème": ["définir le problème", "analyser les causes", "proposer une solution"],
        "génération": ["comprendre le type de contenu", "structurer les idées", "produire une réponse"],
        "créatif": ["explorer les inspirations", "structurer l'idée", "créer la proposition"]
    }

    def planifier(self, intention: str, objectif: str) -> list:
        """Retourne un plan structuré en étapes selon le type d’intention."""
        phases = self.PHASES_STANDARD.get(intention.lower(), ["analyser le besoin", "répondre", "conclure"])
        return [{"étape": phase, "status": "à faire"} for phase in phases]

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "").lower()
        objectif = ctx.get("objectif", {}).get("but", "").lower()

        if not intention or not objectif:
            ctx.setdefault("plugins_log", []).append("plugin_planificateur_contextuel : intention/objectif manquant")
            return ctx

        plan = self.planifier(intention, objectif)
        ctx["plan"] = plan
        ctx["tache_courante"] = plan[0]["étape"] if plan else "inconnu"
        ctx.setdefault("plugins_log", []).append("plugin_planificateur_contextuel : plan généré")
        logger.info(f"[planificateur] Plan établi ({len(plan)} étapes) pour intention : {intention}")

        return ctx
