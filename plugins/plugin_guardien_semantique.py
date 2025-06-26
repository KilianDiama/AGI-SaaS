from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.guardien_semantique")

class PluginGuardienSemantique(BasePlugin):
    meta = Meta(
        name="plugin_guardien_semantique",
        version="1.0",
        priority=1.6,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "").strip()
        reponse = ctx.get("response", "").strip()
        intention = ctx.get("intention", "")
        reflexion = ctx.get("reflexion_interne", "")
        synthese = ctx.get("synthese_contextuelle", "")

        alertes = []

        if "je ne sais pas" in reponse.lower() and "informer" in intention.lower():
            alertes.append("⚠️ Incohérence : l'IA avoue ne pas savoir alors qu’elle doit informer.")

        if "aucune tâche" in reflexion.lower() and ctx.get("tache_courante"):
            alertes.append("🔁 Contradiction : réflexion dit 'aucune tâche' mais une tâche est définie.")

        if message and not reponse:
            alertes.append("❌ Alerte : message utilisateur reçu mais aucune réponse générée.")

        if "inconnu" in synthese.lower():
            alertes.append("🧩 Synthèse partiellement vide : données manquantes ou mal extraites.")

        if alertes:
            ctx["alertes_semantiques"] = alertes
            ctx.setdefault("plugins_log", []).append("PluginGuardienSemantique : incohérences détectées.")
            logger.warning(f"[guardien_semantique] Alerte(s) détectée(s) : {len(alertes)}")
        else:
            ctx.setdefault("plugins_log", []).append("PluginGuardienSemantique : aucune incohérence trouvée.")

        return ctx
