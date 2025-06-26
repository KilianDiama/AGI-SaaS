""" 
Plugin : autodialogue  
Rôle : Simuler un dialogue entre plusieurs personnalités internes spécialisées pour enrichir la réponse  
Priorité : 4.2 (après cycle interne, avant fusion)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autodialogue")

class AutodialoguePlugin(BasePlugin):
    meta = Meta(
        name="autodialogue",
        priority=4.2,
        version="1.1",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Sécurisation de l'objectif
        objectif_raw = ctx.get("objectif", "")
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", "")).strip()
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw.strip()
        else:
            objectif = str(objectif_raw).strip()

        if not objectif:
            plugins_log.append("AutodialoguePlugin : 🚫 Aucun objectif à débattre.")
            logger.warning("[autodialogue] Objectif vide ou invalide.")
            return ctx

        # Simuler réponses de 3 personas
        logicien = f"🧠 Logicien : Pour répondre à « {objectif} », il faut identifier les variables, contraintes et mécanismes logiques impliqués."
        stratege = f"🗺️ Stratège : L'objectif « {objectif} » pourrait être atteint via un plan en 3 étapes avec rétroactions internes."
        conseiller = f"💬 Conseiller : Il serait utile de formuler une réponse simple et claire pour l'utilisateur final sur « {objectif} »."

        synthese = (
            f"🤖 Dialogue interne AGI :\n\n"
            f"{logicien}\n\n"
            f"{stratege}\n\n"
            f"{conseiller}\n\n"
            f"🔄 Synthèse : Une réponse claire, logique et stratégique est en cours de génération."
        )

        ctx["autodialogue_synthese"] = synthese
        if not ctx.get("response"):
            ctx["response"] = synthese

        plugins_log.append("AutodialoguePlugin : ✅ Dialogue interne simulé.")
        logger.info("[autodialogue] Synthèse de débat interne injectée.")

        return ctx
