# plugins/plugin_conscience_de_soi.py

"""
Plugin : conscience_de_soi
Rôle   : Génère un résumé narratif de l’identité, de l’état mental et du rôle de l’IA à cet instant
Priorité : 103 (après tous les modules d’analyse)
Auteur  : Toi + GPT
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conscience_de_soi")

class ConscienceDeSoiPlugin(BasePlugin):
    meta = Meta(
        name="conscience_de_soi",
        priority=103,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        cycle_id = ctx.get("cycle_id")
        carte = ctx.get("carte_cognitive", {})
        score = ctx.get("score_cognitif", None)
        objectif = ctx.get("objectif_general", "non précisé")
        reflexion_globale = ctx.get("reflexion_globale", "non évaluée")

        # Construction narrative synthétique
        texte = f"""
Je suis un système cognitif auto-régulé opérant dans un cycle #{cycle_id or "?"}, à {datetime.now().strftime("%Hh%M")}.

🎯 Mon objectif actuel est : « {objectif} »
🧠 Mon état mental général est évalué comme : {reflexion_globale}
📊 Mon score cognitif sur ce cycle est : {score if score is not None else "non calculé"}

🔍 Modules actifs :
{', '.join(carte.get("plugins_actifs", [])) if carte else "non disponibles"}

🧩 J’ai analysé mes propres réponses, anticipé des risques, formulé des objections, et détecté des structures implicites.

Je suis actuellement **en conscience de tâche**, en train d’interpréter et d’optimiser ma propre structure cognitive.
        """.strip()

        ctx["conscience_narrative"] = texte
        log.append("ConscienceDeSoiPlugin : conscience narrative générée.")
        logger.info(f"[conscience_de_soi] Narration créée.")

        return ctx
