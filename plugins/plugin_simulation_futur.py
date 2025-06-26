# plugins/plugin_simulation_futur.py
from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.simulation_futur")

class PluginSimulationFutur(BasePlugin):
    meta = Meta(
        name="plugin_simulation_futur",
        version="1.0",
        priority=98.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("demande_llm") or ctx.get("llm_prompt", "")
        reponse = ctx.get("llm_response", "")

        if not message or not reponse:
            ctx.setdefault("plugins_log", []).append("PluginSimulationFutur : pas assez de données pour simuler.")
            return ctx

        simulation_prompt = (
            f"À partir de l'objectif '{ctx.get('objectif', 'non spécifié')}', "
            f"du message utilisateur '{message}' et de la réponse '{reponse}', "
            "génère 3 scénarios de conséquences : un optimiste, un incertain, un négatif. "
            "Pour chaque, donne un titre, une description, l'impact et une estimation de probabilité (0.0 à 1.0)."
        )

        ctx["llm_prompt"] = simulation_prompt
        ctx["simulation_futur"] = {
            "date": datetime.now().isoformat(),
            "scenarios": []  # rempli dans le plugin LLM suivant
        }
        ctx.setdefault("plugins_log", []).append("PluginSimulationFutur : prompt de simulation généré.")
        return ctx
