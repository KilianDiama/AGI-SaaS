import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.context_supervisor")

class PluginContextSupervisor(BasePlugin):
    meta = Meta(
        name="plugin_context_supervisor",
        version="1.0",
        priority=1.1,  # Juste après auth/mémoire, avant analyse
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Purge des entrées vides ou corrompues
        for key in ["objectif", "intention", "reflexion_interne", "response_logique", "memoire_contextuelle"]:
            if ctx.get(key) in ("", None, [], {}):
                ctx.pop(key, None)
                logger.info(f"[ContextSupervisor] Nettoyage clé vide : {key}")

        # Normalisation du plan
        plan = ctx.get("plan", [])
        if isinstance(plan, list):
            cleaned_plan = [step for step in plan if "étape" in step and step.get("status") != "annulé"]
            ctx["plan"] = cleaned_plan

        # Nettoyage historique inutile
        history = ctx.get("history", [])
        if len(history) > 20:
            ctx["history"] = history[-20:]
            logger.info("[ContextSupervisor] Historique réduit à 20 derniers échanges")

        # Conflit potentiel
        intention = ctx.get("intention", "")
        if "analyser" in intention and "synthétiser" in intention:
            ctx["intention"] = "analyse + synthèse"
            logger.info("[ContextSupervisor] Intention clarifiée : analyse + synthèse")

        ctx.setdefault("plugins_log", []).append("PluginContextSupervisor : contexte nettoyé et stabilisé")
        return ctx
