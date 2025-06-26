# plugins/plugin_multi_agent_controller.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.multi_agent_controller")

class PluginMultiAgentController(BasePlugin):
    meta = Meta(
        name="plugin_multi_agent_controller",
        version="1.0",
        priority=40.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("llm_prompt") or ctx.get("response") or ctx.get("demande_llm")
        if not message:
            ctx.setdefault("plugins_log", []).append("MultiAgent : aucun message à analyser.")
            return ctx

        roles = {
            "Chercheur": "Explore les connaissances pertinentes sur le sujet.",
            "Analyste": "Décompose le problème en sous-problèmes logiques.",
            "Critique": "Évalue la qualité, la logique et les limites de la solution proposée."
        }

        responses = []
        from plugins.utils.llm_call import call_llm_main
        for role, instruction in roles.items():
            prompt = f"Rôle : {role}\nInstruction : {instruction}\nMessage utilisateur : {message}"
            try:
                resp = await call_llm_main(ctx, prompt)
                responses.append(f"{role} : {resp.strip()}")
                ctx.setdefault("plugins_log", []).append(f"MultiAgent : {role} a répondu.")
            except Exception as e:
                logger.warning(f"[MultiAgent] Erreur avec {role} : {e}")

        ctx["response"] = "\n\n".join(responses)
        return ctx
