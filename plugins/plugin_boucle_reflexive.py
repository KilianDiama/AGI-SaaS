# plugins/plugin_boucle_reflexive.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.boucle_reflexive")

class PluginBoucleReflexive(BasePlugin):
    meta = Meta(
        name="plugin_boucle_reflexive",
        version="1.0",
        priority=99.8,  # tout à la fin du cycle
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        note = ctx.get("evaluation_reponse", {}).get("note", 0)
        objectif = ctx.get("objectif", {}).get("but", "")
        reponse = ctx.get("response", "").strip()

        if note >= 3 or not objectif or not reponse:
            ctx.setdefault("plugins_log", []).append("BoucleReflexive : aucune relance nécessaire.")
            return ctx

        # Déclenche une boucle d’amélioration si qualité perçue faible
        boucle_prompt = f"""La réponse suivante est faible (note = {note}/5) pour l’objectif : « {objectif} ».

Réponse actuelle :
---
{reponse}
---

Propose une meilleure réponse. Sois plus clair, structuré, utile.
"""
        from plugins.utils.llm_call import call_llm_main
        nouvelle_reponse = (await call_llm_main(ctx, boucle_prompt)).strip()

        if nouvelle_reponse:
            ctx["response"] = nouvelle_reponse
            ctx.setdefault("plugins_log", []).append("BoucleReflexive : réponse améliorée automatiquement.")
        else:
            ctx.setdefault("plugins_log", []).append("BoucleReflexive : amélioration échouée.")

        return ctx
