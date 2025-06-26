from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.contexte_superviseur")

class PluginContexteSuperviseur(BasePlugin):
    meta = Meta(
        name="plugin_contexte_superviseur",
        version="1.0",
        priority=4.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        intention = ctx.get("intention", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        resume = ctx.get("memoire_contextuelle", "")

        ajustements = []

        if not historique:
            ajustements.append("📭 Aucune mémoire conversationnelle détectée.")
        if intention in ["", None, "vide"]:
            ajustements.append("🧠 Intention à recalibrer : penser à reformuler ou demander confirmation.")
        if objectif in ["", "répondre à une question générale", None]:
            ajustements.append("🎯 Objectif trop vague → suggestion : préciser l’intention utilisateur.")
        if len(resume.strip()) < 10:
            ajustements.append("🧾 Résumé contextuel insuffisant pour une continuité efficace.")

        ctx["contexte_supervision"] = "\n".join(ajustements)
        ctx.setdefault("plugins_log", []).append("PluginContexteSuperviseur : supervision effectuée.")
        logger.info(f"[contexte_superviseur] Ajustements proposés :\n" + "\n".join(ajustements))

        return ctx
