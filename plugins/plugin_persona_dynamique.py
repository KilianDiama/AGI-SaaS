from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.persona_dynamique")

class PluginPersonaDynamique(BasePlugin):
    meta = Meta(
        name="plugin_persona_dynamique",
        version="1.0",
        priority=2.05,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("memoire_contextuelle", "").lower()
        persona = "neutre"

        if "urgent" in historique or "vite" in historique:
            persona = "direct"
        elif "❤️" in historique or "mon amour" in historique:
            persona = "affectueux"
        elif "code" in historique or "erreur" in historique:
            persona = "technique"
        elif "poème" in historique or "inspire-moi" in historique:
            persona = "créatif"
        elif "simplifie" in historique or "explique-moi" in historique:
            persona = "pédagogue"

        ctx["persona_actif"] = persona
        ctx.setdefault("plugins_log", []).append(f"PluginPersonaDynamique : persona détecté → {persona}")
        logger.info(f"[persona dynamique] Persona sélectionné : {persona}")
        return ctx
