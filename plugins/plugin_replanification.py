import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.replanification")

class PluginReplanification(BasePlugin):
    meta = Meta(
        name="plugin_replanification",
        version="1.0",
        priority=2.8,  # Après le planificateur, avant le raisonneur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        etape = ctx.get("tache_courante", "")
        note_eval = ctx.get("evaluation_reponse", {}).get("note", 1.0)
        reflex = ctx.get("reflexion_interne", "")

        ctx.setdefault("plugins_log", [])

        # Cas 1 : réponse notée 0 → échec clair
        if note_eval == 0:
            logger.warning("[replanification] Réponse vide ou invalide détectée.")
            new_plan = self._generer_plan_secours(etape)
            ctx["plan"] = new_plan
            ctx["tache_courante"] = new_plan[0]["étape"]
            ctx["plugins_log"].append("plugin_replanification : plan de secours généré (réponse nulle)")
            return ctx

        # Cas 2 : blocage détecté dans la réflexion
        if "aucune tâche" in reflex.lower() or "pause" in reflex.lower():
            logger.warning("[replanification] Blocage détecté via réflexion.")
            new_plan = self._generer_plan_secours(etape)
            ctx["plan"] = new_plan
            ctx["tache_courante"] = new_plan[0]["étape"]
            ctx["plugins_log"].append("plugin_replanification : plan de secours généré (reflexion)")
            return ctx

        ctx["plugins_log"].append("plugin_replanification : aucun blocage détecté")
        return ctx

    def _generer_plan_secours(self, ancienne_etape: str):
        return [
            {"étape": "réexaminer les intentions", "status": "à faire"},
            {"étape": "analyser le contexte actuel", "status": "à faire"},
            {"étape": "formuler une nouvelle stratégie", "status": "à faire"},
            {"étape": f"reprise depuis : {ancienne_etape}", "status": "à faire"},
        ]
