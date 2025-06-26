# plugins/raisonnement/plugin_reflex.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.reflex")

class PluginReflex(BasePlugin):
    meta = Meta(
        name="plugin_reflex",
        priority=1.5,  # Position intermédiaire, après intention, avant raisonnement
        version="2.0",
        author="Fusion Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        plan = ctx.get("plan", [])
        etape = ctx.get("tache_courante", "")
        messages = []

        # 1. Réflexion sur l’intention
        if not intention or intention.lower() in {"", "vide"}:
            messages.append("❓ Intention incertaine. Clarifiez ou reformulez la demande.")

        # 2. Réflexion sur l’objectif
        if not objectif or objectif.lower() in {"", "répondre à une question générale"}:
            messages.append("🔍 Objectif trop générique. Envisager une formulation plus précise.")

        # 3. État du plan
        if not plan:
            messages.append("⚠️ Aucun plan détecté. Risque de non-action.")
        elif all(step.get("status") == "fait" for step in plan):
            messages.append("✅ Toutes les étapes du plan sont terminées. Rien à faire.")
        else:
            # Ajouter résumé rapide du plan
            steps = [f"- {step.get('étape')} ({step.get('status')})" for step in plan]
            messages.append("📋 Plan détecté :\n" + "\n".join(steps))

        # 4. Étape courante
        if etape:
            messages.append(f"📌 Étape actuelle : {etape}")
        else:
            messages.append("⛔ Aucune tâche active. Vérifier le cycle.")

        # Injection dans le contexte
        commentaire = "\n".join(messages)
        ctx["reflexion_interne"] = commentaire
        ctx.setdefault("plugins_log", []).append("PluginReflex : réflexion injectée.")
        logger.info(f"[reflex] Réflexion système :\n{commentaire}")

        return ctx
