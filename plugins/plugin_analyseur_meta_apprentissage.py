# plugins/plugin_analyseur_meta_apprentissage.py

from noyau_core import BasePlugin, Context, Meta
from collections import defaultdict, Counter

class PluginAnalyseurMetaApprentissage(BasePlugin):
    meta = Meta(
        name="plugin_analyseur_meta_apprentissage",
        version="1.0",
        priority=2.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        trace = ctx.get("meta_trace_apprentissage", [])
        if not trace:
            ctx["plugins_log"].append("PluginAnalyseurMetaApprentissage : aucune trace à analyser.")
            return ctx

        action_scores = defaultdict(list)

        for entry in trace:
            actions = entry.get("actions", [])
            note = entry.get("note", 0)
            for act in actions:
                action_scores[act].append(note)

        moyennes = {
            action: round(sum(scores) / len(scores), 2)
            for action, scores in action_scores.items()
            if scores
        }

        top_actions = sorted(moyennes.items(), key=lambda x: x[1], reverse=True)[:3]
        worst_actions = sorted(moyennes.items(), key=lambda x: x[1])[:3]

        ctx["meta_apprentissage_stats"] = {
            "meilleures_actions": top_actions,
            "pires_actions": worst_actions,
            "actions_analysees": len(action_scores)
        }

        ctx["plugins_log"].append(f"PluginAnalyseurMetaApprentissage : top actions = {top_actions}")
        return ctx
