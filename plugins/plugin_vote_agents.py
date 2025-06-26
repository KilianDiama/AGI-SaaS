# plugins/plugin_vote_agents.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.vote_agents")

class PluginVoteAgents(BasePlugin):
    meta = Meta(
        name="plugin_vote_agents",
        version="1.0",
        priority=42.0,  # après génération de réponses, avant fusion
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        hypotheses = ctx.get("hypotheses_multiples", [])
        if not hypotheses or len(hypotheses) < 2:
            ctx.setdefault("plugins_log", []).append("VoteAgents : pas assez d'hypothèses pour voter.")
            return ctx

        prompt_vote = f"""Tu es un jury d’experts IA.

Voici plusieurs propositions de réponse à une même question utilisateur :
{chr(10).join(f"Hypothèse {i+1} : {h}" for i, h in enumerate(hypotheses))}

Analyse chaque réponse (clarté, pertinence, structure, style) et vote pour la meilleure.
Formate ta réponse comme ceci :
- Gagnante : Hypothèse X
- Justification : ..."""

        try:
            from plugins.utils.llm_call import call_llm_main
            decision = await call_llm_main(ctx, prompt_vote)
            ctx["vote_agents"] = decision

            # récupération automatique de l’hypothèse gagnante si identifiable
            for i in range(len(hypotheses)):
                if f"Hypothèse {i+1}" in decision:
                    ctx["response"] = hypotheses[i]
                    break

            ctx.setdefault("plugins_log", []).append("VoteAgents : vote effectué.")
        except Exception as e:
            logger.error(f"[VoteAgents] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append("VoteAgents : erreur de vote.")

        return ctx
