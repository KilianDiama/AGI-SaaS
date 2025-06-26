from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.attention_contextuelle")

class PluginAttentionContextuelle(BasePlugin):
    meta = Meta(
        name="plugin_attention_contextuelle",
        version="1.0",
        priority=1.3,  # Avant réflexion, raisonneur, etc.
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        resume = ctx.get("memoire_contextuelle", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        plan = ctx.get("plan", [])

        injections = []

        if historique:
            dernier = historique[-1]
            injections.append(f"🕓 Dernier message :\n{dernier.get('message', '')}")

        if resume:
            injections.append(f"🧠 Mémoire contextuelle :\n{resume}")

        if objectif:
            injections.append(f"🎯 Objectif en cours : {objectif}")

        if plan:
            étapes = [f"{e['étape']} ({e['status']})" for e in plan]
            injections.append(f"📋 Plan actuel :\n" + "\n".join(étapes))

        bloc_contexte = "\n\n".join(injections)

        if bloc_contexte:
            ctx["context_injection"] = bloc_contexte
            ctx.setdefault("plugins_log", []).append("PluginAttentionContextuelle : contexte injecté.")
            logger.info("[AttentionContextuelle] Contexte intégré au raisonnement.")
        else:
            ctx.setdefault("plugins_log", []).append("PluginAttentionContextuelle : aucun contexte à injecter.")
        
        return ctx
