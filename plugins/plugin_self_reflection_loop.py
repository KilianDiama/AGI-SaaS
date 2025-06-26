# plugins/plugin_self_reflection_loop.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.self_reflection_loop")

class PluginSelfReflectionLoop(BasePlugin):
    meta = Meta(
        name="plugin_self_reflection_loop",
        version="1.0",
        priority=45.0,  # après génération initiale, avant finalisation
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        original_response = ctx.get("response", "").strip()
        if not original_response:
            ctx.setdefault("plugins_log", []).append("SelfReflectionLoop : pas de réponse à réfléchir.")
            return ctx

        prompt = f"""Tu es un assistant intelligent capable d’auto-amélioration.
Voici une réponse que tu viens de produire :

--- Réponse initiale ---
{original_response}
-------------------------

1. Détecte toute faiblesse (manque de clarté, longueur, ambiguïté, incohérence…).
2. Suggère une version améliorée si nécessaire.

Formate ta réponse ainsi :
- Faiblesses : ...
- Nouvelle version : ...
"""

        try:
            from plugins.utils.llm_call import call_llm_main
            reflexion = await call_llm_main(ctx, prompt)
            ctx["reflexion"] = reflexion
            if "Nouvelle version" in reflexion:
                nouvelle = reflexion.split("Nouvelle version :")[1].strip()
                ctx["response"] = nouvelle
            ctx.setdefault("plugins_log", []).append("SelfReflectionLoop : réflexion effectuée.")
        except Exception as e:
            logger.error(f"[SelfReflectionLoop] Erreur : {e}")

        return ctx
