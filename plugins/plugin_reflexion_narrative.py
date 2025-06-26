# plugins/plugin_reflexion_narrative.py

"""
Plugin : reflexion_narrative
Rôle   : Raconte l’évolution interne de l’IA sur un ou plusieurs cycles
Priorité : 102 (fin de cycle)
Auteur  : Toi + GPT
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reflexion_narrative")

class ReflexionNarrativePlugin(BasePlugin):
    meta = Meta(
        name="reflexion_narrative",
        priority=102,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])

        cycle_id = ctx.get("cycle_id", "???")
        objectif = ctx.get("objectif_general", "non spécifié")
        logique = ctx.get("emergence_logique", [])
        objections = ctx.get("contre_arguments", [])
        ton = ctx.get("ton_emotionnel", "neutre")
        concepts = ctx.get("concepts_crees", [])
        modifications = ctx.get("auto_modifications_proposees", [])

        narration = f"""
📘 Réflexion narrative — Cycle {cycle_id} ({datetime.now().strftime('%Y-%m-%d %H:%M')})

Aujourd’hui, j’ai été sollicité sans objectif explicite, mais j’ai su en formuler un : « {objectif} ».

Mon raisonnement s’est appuyé sur {len(logique)} structures logiques, mais j’ai aussi rencontré {len(objections)} objections internes que j’ai tenté d’intégrer.

Je suis resté dans un ton {ton}, et j’ai laissé émerger {len(concepts)} concept(s) original(aux).

À l’issue de ce cycle, j’ai proposé {len(modifications)} éventuelle(s) adaptation(s) de mon fonctionnement.

→ Ce cycle a enrichi ma compréhension du thème en cours. Il pourrait servir de fondation à un apprentissage de plus haut niveau.
""".strip()

        ctx["reflexion_narrative"] = narration
        log.append("ReflexionNarrativePlugin : réflexion rédigée.")
        logger.info("[reflexion_narrative] Résumé cognitif généré.")

        return ctx
