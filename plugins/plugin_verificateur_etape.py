import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.verificateur_etape")

class PluginVerificateurEtape(BasePlugin):
    meta = Meta(
        name="plugin_verificateur_etape",
        version="1.0",
        priority=1.36,  # Après prédicteur, avant changement d'étape
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        current_step = ctx.get("tache_courante", "")
        output = ctx.get("llm_response", "") or ctx.get("response", "")
        logs = ctx.setdefault("plugins_log", [])
        plan = ctx.get("plan", [])

        if not current_step or not plan:
            logs.append("PluginVerificateurEtape : tâche ou plan manquant.")
            return ctx

        # Vérification simple par présence de contenu (améliorable avec heuristiques)
        if output and len(output.strip()) > 10:
            for step in plan:
                if step["étape"] == current_step:
                    step["status"] = "fait"
                    logs.append(f"PluginVerificateurEtape : étape '{current_step}' validée ✅.")
                    logger.info(f"[verificateur_etape] Étape validée : {current_step}")
                    break
        else:
            logs.append(f"PluginVerificateurEtape : sortie insuffisante pour valider l'étape '{current_step}' ❌.")

        return ctx
