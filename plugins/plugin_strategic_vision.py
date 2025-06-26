from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.strategic_vision")

class PluginStrategicVision(BasePlugin):
    meta = Meta(
        name="plugin_strategic_vision",
        version="1.0",
        priority=1.7,  # Après analyse intention, avant planification
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip().lower()
        plan = ctx.get("plan", [])
        messages = []

        # Vérifie si le plan est vide ou sans lien avec l'objectif
        if not plan:
            messages.append("⚠️ Aucun plan détecté pour l’objectif → risque de stagnation.")
            plan = self.suggere_plan_par_defaut(objectif)
            ctx["plan"] = plan
            messages.append(f"🧠 Nouveau plan injecté ({len(plan)} étapes).")

        # Vérifie si toutes les étapes sont "à faire" ou "en pause"
        if all(etape.get("status", "") in ("à faire", "en pause") for etape in plan):
            messages.append("⏸️ Plan inactif détecté → proposer un redémarrage ciblé.")
            ctx["tache_courante"] = plan[0]["étape"] if plan else "réflexion stratégique"

        # Analyse sémantique de l’objectif
        if "question" in objectif or "informer" in objectif:
            messages.append("🎯 Objectif = information → planification légère recommandée.")
        elif "résoudre" in objectif or "problème" in objectif:
            messages.append("🔧 Objectif = résolution → plan structuré essentiel.")

        ctx["vision_stratégique"] = "\n".join(messages)
        ctx.setdefault("plugins_log", []).append("plugin_strategic_vision : diagnostic plan réalisé.")
        logger.info(f"[vision] Diagnostic stratégique :\n{ctx['vision_stratégique']}")

        return ctx

    def suggere_plan_par_defaut(self, objectif: str):
        if "question" in objectif:
            return [
                {"étape": "identifier le sujet", "status": "à faire"},
                {"étape": "extraire les infos pertinentes", "status": "à faire"},
                {"étape": "formuler une réponse claire", "status": "à faire"}
            ]
        elif "résoudre" in objectif:
            return [
                {"étape": "analyser le problème", "status": "à faire"},
                {"étape": "évaluer les solutions", "status": "à faire"},
                {"étape": "exécuter la solution retenue", "status": "à faire"}
            ]
        else:
            return [
                {"étape": "clarifier l’intention", "status": "à faire"},
                {"étape": "proposer une direction", "status": "à faire"}
            ]
