# plugins/plugin_creativite_strategique.py
from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.creativite_strategique")

class PluginCreativiteStrategique(BasePlugin):
    meta = Meta(
        name="plugin_creativite_strategique",
        version="1.0",
        priority=98.1,
        author="Toi & GPT"
    )

    STRATEGIES = [
        "Et si on faisait l’inverse ?",
        "Fusionnons deux idées opposées.",
        "Quelles sont les hypothèses implicites à briser ?",
        "Comment un enfant verrait cette situation ?",
        "Imaginons que la solution soit vivante, que ferait-elle ?",
        "Si une IA maline sabotait ça, comment elle s’y prendrait ?",
        "Quelle est l’option la plus absurde mais intrigante ?"
    ]

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "")
        prompt = ctx.get("llm_prompt", "")
        situation = ctx.get("memoire_contextuelle", "")

        if not prompt or not intention:
            return ctx

        idee_creative = random.choice(self.STRATEGIES)

        reflexion = f"💡 Idée créative : {idee_creative} Appliquons-la à cette situation : {situation or prompt}"

        ctx.setdefault("reflexions_creatives", []).append(reflexion)
        ctx.setdefault("plugins_log", []).append("PluginCreativiteStrategique : idée injectée.")
        ctx["llm_prompt"] += f"\n\n🧠 Réflexion créative suggérée :\n{reflexion}"

        return ctx
