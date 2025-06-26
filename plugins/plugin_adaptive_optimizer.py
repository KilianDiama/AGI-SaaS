from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.adaptive_optimizer")

class PluginAdaptiveOptimizer(BasePlugin):
    meta = Meta(
        name="plugin_adaptive_optimizer",
        version="1.0",
        priority=4.9,  # Avant dernière étape
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logs = ctx.setdefault("plugins_log", [])
        note = ctx.get("evaluation_reponse", {}).get("note", 0)
        temps_total = (ctx.get("ts_end") or 0) and (ctx.get("ts_start") or 0)
        dynamic_compo = ctx.get("composition_dynamique", [])
        auto_plugins = []

        # 🧠 Suggestion : charger des plugins supplémentaires selon note
        if note <= 2:
            if "plugin_verificateur_reponse" not in dynamic_compo:
                auto_plugins.append("plugin_verificateur_reponse")
            if "plugin_prompt_refiner" not in dynamic_compo:
                auto_plugins.append("plugin_prompt_refiner")

        # ⏱️ Suggestion : mode rapide si réponse trop lente
        if isinstance(temps_total, float) and temps_total > 10:
            ctx["performance_mode"] = "fast"
            logs.append("PluginAdaptiveOptimizer : bascule en mode performance rapide.")

        # 🔁 Mise à jour des plugins actifs
        if auto_plugins:
            ctx.setdefault("plugins_forcés", []).extend(auto_plugins)
            logs.append(f"PluginAdaptiveOptimizer : plugins ajoutés dynamiquement → {auto_plugins}")

        # 🧭 Marquage global
        ctx["optimizator_status"] = "optimisation appliquée" if auto_plugins else "aucun changement nécessaire"
        logger.info("[adaptive_optimizer] Ajustement dynamique terminé.")
        return ctx
