"""
Plugin : simulation_et_si
Rôle : Simuler des alternatives mentales pour tester les conséquences avant d’agir
Priorité : 3.5 (entre réflexion et réponse)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.simulation_et_si")

class SimulationEtSiPlugin(BasePlugin):
    meta = Meta(
        name="simulation_et_si",
        priority=3.5,
        version="1.0",
        author="AGI & Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")

        if not message or "et si" not in message.lower():
            plugins_log.append("SimulationEtSiPlugin : pas de scénario hypothétique à traiter.")
            return ctx

        hypothese = message.strip()
        reponse_simulee = f"→ Hypothèse détectée : '{hypothese}'.\nRésultat simulé : " \
                          f"Si cette action est prise, cela pourrait entraîner un changement de comportement, " \
                          f"une nouvelle branche logique, ou une réponse différente."

        ctx["simulation_et_si"] = reponse_simulee
        plugins_log.append("SimulationEtSiPlugin : simulation hypothétique formulée.")
        logger.info("[simulation_et_si] Simulation générée.")

        return ctx
