import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.multi_hypotheses")

class PluginMultiHypotheses(BasePlugin):
    meta = Meta(
        name="plugin_multi_hypotheses",
        version="1.0",
        priority=3.7,  # Après les LLM mais avant le vote / fusion
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base_message = ctx.get("message", "")
        llm_outputs = ctx.get("llm_responses", [])
        logic = ctx.get("response_logique", "")
        reflex = ctx.get("reflexion_interne", "")

        hypotheses = []

        # Source : LLM multiples
        for rep in llm_outputs:
            if rep.strip():
                hypotheses.append(rep.strip())

        # Source : raisonnement logique
        if logic and logic not in hypotheses:
            hypotheses.append(f"[logique]\n{logic.strip()}")

        # Source : réflexion
        if reflex and reflex not in hypotheses:
            hypotheses.append(f"[réflexion]\n{reflex.strip()}")

        # Injection
        if hypotheses:
            ctx["hypotheses_multiples"] = hypotheses
            plugins_log.append(f"plugin_multi_hypotheses : {len(hypotheses)} hypothèses collectées")
            logger.info(f"[plugin_multi_hypotheses] {len(hypotheses)} générées :\n" + "\n\n---\n".join(hypotheses))
        else:
            plugins_log.append("plugin_multi_hypotheses : aucune hypothèse trouvée")

        return ctx
