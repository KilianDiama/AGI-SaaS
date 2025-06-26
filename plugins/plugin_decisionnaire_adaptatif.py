# plugins/plugin_decisionnaire_adaptatif.py

from noyau_core import BasePlugin, Context, Meta

class PluginDecisionnaireAdaptatif(BasePlugin):
    meta = Meta(
        name="plugin_decisionnaire_adaptatif",
        version="1.0",
        priority=2.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        actions = ctx.get("meta_actions", [])
        log = ctx.setdefault("plugins_log", [])

        if not actions:
            log.append("PluginDecisionnaireAdaptatif : aucune action à appliquer.")
            return ctx

        ctx.setdefault("actions_appliquees", [])
        for action in actions:
            if "température" in action.lower():
                current = ctx["llm_config"].get("temperature", 0.7)
                ctx["llm_config"]["temperature"] = min(current + 0.1, 1.5)
                log.append(f"PluginDecisionnaireAdaptatif : température augmentée → {ctx['llm_config']['temperature']}")
                ctx["actions_appliquees"].append("température++")

            elif "critique automatique" in action.lower():
                ctx["mode_critique_auto"] = True
                log.append("PluginDecisionnaireAdaptatif : mode critique activé.")
                ctx["actions_appliquees"].append("critique_auto")

            elif "simplifier" in action.lower():
                ctx["style_instruction"] = "phrases simples, ton direct, moins de 20 mots par phrase."
                log.append("PluginDecisionnaireAdaptatif : style simplifié.")
                ctx["actions_appliquees"].append("style_simplifié")

        return ctx
