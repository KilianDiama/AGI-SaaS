# plugins/plugin_suivi_performance_plugins.py

from noyau_core import BasePlugin, Context, Meta
import time

class PluginSuiviPerformancePlugins(BasePlugin):
    meta = Meta(
        name="plugin_suivi_performance_plugins",
        version="1.0",
        priority=99.9,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.get("plugins_log", [])
        scores = {}
        response = ctx.get("llm_response", "").strip()

        if not response:
            plugins_log.append(f"{self.meta.name} : aucune réponse LLM — score global = 0")
            return ctx

        note = ctx.get("evaluation_reponse", {}).get("note", 0)

        for log in plugins_log:
            if ":" in log:
                plugin_name = log.split(":")[0].strip()
                scores.setdefault(plugin_name, 0)
                if "injecté" in log or "réponse" in log or "ajustement" in log:
                    scores[plugin_name] += 1

        performance = {p: round(s * (note / 5), 2) for p, s in scores.items()}
        ctx["plugin_performance"] = performance
        plugins_log.append(f"{self.meta.name} : scores plugins → {performance}")
        return ctx
