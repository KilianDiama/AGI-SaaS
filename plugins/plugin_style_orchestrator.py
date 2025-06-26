import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.style_orchestrator")

class PluginStyleOrchestrator(BasePlugin):
    meta = Meta(
        name="plugin_style_orchestrator",
        version="1.0",
        priority=2.6,  # Avant le raffinage ou génération LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "").lower()
        style = "neutre"
        ton = "clair"
        niveau = "intermédiaire"

        # 🎭 Adapte en fonction de l’intention
        if "motivation" in intention or "coaching" in intention:
            ton = "chaleureux"
            style = "enthousiaste"
            niveau = "accessible"

        elif "technique" in intention or "explication" in intention:
            style = "structuré"
            ton = "didactique"
            niveau = "avancé"

        elif "vente" in intention or "promotion" in intention:
            style = "persuasif"
            ton = "convaincant"

        # 🔁 Historique utilisateur ou config personnalisée ?
        config_style = ctx.get("user_config", {}).get("style_instruction")
        if config_style:
            ctx["style_instruction"] = config_style
            logger.info("[style_orchestrator] Style défini par config utilisateur.")
        else:
            ctx["style_instruction"] = f"Tu dois répondre avec un ton **{ton}**, un style **{style}**, et un niveau de complexité **{niveau}**."
            logger.info(f"[style_orchestrator] Style injecté automatiquement → ton={ton}, style={style}, niveau={niveau}")

        ctx.setdefault("plugins_log", []).append("plugin_style_orchestrator : style injecté dynamiquement")
        return ctx
