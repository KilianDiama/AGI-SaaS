# plugins/plugin_mutation_pipeline.py

from noyau_core import BasePlugin, Context, Meta
import random

class PluginMutationPipeline(BasePlugin):
    meta = Meta(
        name="plugin_mutation_pipeline",
        version="1.0",
        priority=98.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        performance = ctx.get("plugin_performance", {})
        objectif = ctx.get("objectif", {}).get("but", "")
        plugins_log = ctx.get("plugins_log", [])

        # Seuil arbitraire pour considérer un plugin peu utile
        low_perf_plugins = [k for k, v in performance.items() if v < 0.5]

        # Plugins candidats à l'ajout
        candidats = [
            "plugin_raisonneur", "plugin_synthese_active", "plugin_prompt_refiner",
            "plugin_coherence_intentionnelle", "plugin_multi_hypotheses",
            "plugin_emotion_regulator", "plugin_response_evaluator_plus"
        ]

        # Muter pipeline : désactiver certains, ajouter d'autres
        mutation_log = []
        for plugin in low_perf_plugins:
            mutation_log.append(f"désactivé: {plugin}")
            ctx["plugins_disabled"] = ctx.get("plugins_disabled", []) + [plugin]

        ajout = random.sample(candidats, min(2, len(candidats)))
        mutation_log.extend([f"ajouté: {p}" for p in ajout])
        ctx["plugins_added"] = ajout
        ctx["plugins_log"].append(f"{self.meta.name} : mutation → {mutation_log}")
        return ctx
