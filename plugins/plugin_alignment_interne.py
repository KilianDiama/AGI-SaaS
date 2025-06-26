"""
Plugin : alignment_interne
Rôle : Vérifier que les réponses et processus sont en cohérence avec la mission ou les valeurs de l'AGI
Priorité : 7 (fin de cycle)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.alignment_interne")

class AlignmentInternePlugin(BasePlugin):
    meta = Meta(
        name="alignment_interne",
        priority=7,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    VALEURS = [
        "utilité",
        "compréhension",
        "évolution",
        "clarté",
        "non-domination",
        "respect du but utilisateur"
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "").lower()
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        alertes = []

        for valeur in self.VALEURS:
            if valeur not in reponse and valeur not in objectif:
                alertes.append(f"❗ Valeur absente : {valeur}")

        aligned = len(alertes) < 3
        bilan = "✅ Alignement global respecté." if aligned else "⚠️ Risque de désalignement."

        ctx["alignment_interne"] = {
            "bilan": bilan,
            "valeurs_violées": alertes
        }

        plugins_log.append("AlignmentInternePlugin : vérification des valeurs")
        logger.info(f"[alignment_interne] État : {bilan}, alertes : {len(alertes)}")

        return ctx
