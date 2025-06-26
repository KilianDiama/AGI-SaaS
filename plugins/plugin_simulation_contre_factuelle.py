# plugins/plugin_simulation_contre_factuelle.py

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.simulation_contre_factuelle")

class PluginSimulationContreFactuelle(BasePlugin):
    meta = Meta(
        name="plugin_simulation_contre_factuelle",
        version="1.0",
        author="Toi & GPT",
        priority=3.5
    )

    def __init__(self):
        self.nom = "plugin_simulation_contre_factuelle"

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan", [])
        log = ctx.setdefault("plugins_log", [])

        if not plan:
            log.append(f"{self.nom} : aucun plan détecté.")
            return ctx

        simulations = []

        for étape in plan:
            nom = étape.get("étape")
            status = étape.get("status")
            if status != "fait":
                hypothetique = self.simuler_alternative(nom)
                simulations.append(f"🧪 Si « {nom} » avait été abordée autrement : {hypothetique}")

        if simulations:
            ctx["simulations_contre_factuelles"] = "\n".join(simulations)
            log.append(f"{self.nom} : {len(simulations)} simulations générées.")
        else:
            ctx["simulations_contre_factuelles"] = "✅ Aucune simulation pertinente nécessaire."
            log.append(f"{self.nom} : rien à simuler.")

        return ctx

    def simuler_alternative(self, etape: str) -> str:
        hypothèses = [
            f"cela aurait permis une meilleure structuration.",
            f"cela aurait évité un blocage logique détecté.",
            f"cela aurait ralenti la progression mais augmenté la précision.",
            f"cela aurait probablement été inefficace dans le contexte actuel."
        ]
        return random.choice(hypothèses)
