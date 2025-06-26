# plugins/plugin_evolution_long_terme.py

import datetime
from noyau_core import BasePlugin, Context, Meta

class PluginEvolutionLongTerme(BasePlugin):
    meta = Meta(
        name="plugin_evolution_long_terme",
        version="1.0",
        priority=2.6,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.setdefault("evolution_long_terme", [])
        ajustements = ctx.get("ajustements_comportementaux", [])
        erreurs = ctx.get("tendance_adaptative", {}).get("top_erreurs", [])
        feedback = ctx.get("evaluation_reponse", {}).get("note", None)

        if ajustements or erreurs:
            snapshot = {
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "ajustements": ajustements,
                "erreurs": erreurs,
                "note": feedback
            }
            historique.append(snapshot)
            ctx["evolution_long_terme"] = historique
            ctx.setdefault("plugins_log", []).append(f"PluginEvolutionLongTerme : snapshot ajouté ({len(historique)} au total)")

        else:
            ctx.setdefault("plugins_log", []).append("PluginEvolutionLongTerme : aucun ajustement à mémoriser.")

        return ctx
