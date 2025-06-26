from noyau_core import BasePlugin, Context, Meta
import logging
import statistics

logger = logging.getLogger("plugin.introspection_adaptative")

class PluginIntrospectionAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_introspection_adaptative",
        version="1.0",
        priority=2.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        cycles = ctx.get("memoire_long_terme", {}).get("cycles", [])
        feedback = ctx.get("evaluation_reponse", {})
        performances = ctx.get("profiling", {})

        notes = [cycle.get("evaluation", {}).get("note", 0) for cycle in cycles if "evaluation" in cycle]
        temps = [cycle.get("profiling", {}).get("temps_total", 0) for cycle in cycles if "profiling" in cycle]

        moyenne_note = statistics.mean(notes) if notes else 0
        moyenne_temps = statistics.mean(temps) if temps else 0

        adaptation = {}

        # 🔍 Adaptation du style si moyenne trop basse
        if moyenne_note < 6:
            ctx["style_instruction"] = "Répondre avec clarté, concision et empathie."
            adaptation["style"] = "clarifié"

        # 🚀 Réduction des modèles si temps de réponse trop long
        if moyenne_temps > 5:
            ctx["llm_models"] = ["llama3"]  # Mono-modèle pour accélérer
            adaptation["models"] = "réduit"

        # 🔁 Réajustement du plan si souvent incomplet
        plans_incomplets = sum(
            1 for cycle in cycles if "plan" in cycle and any(e["status"] != "fait" for e in cycle["plan"])
        )
        if plans_incomplets > len(cycles) // 2:
            ctx["forcer_plan_simplifie"] = True
            adaptation["plan"] = "simplifié"

        ctx["adaptation_dynamique"] = adaptation
        ctx.setdefault("plugins_log", []).append("PluginIntrospectionAdaptative : ajustement dynamique appliqué.")
        logger.info(f"[introspection] Adaptations appliquées : {adaptation}")

        return ctx
