"""
Plugin : cycle_interne
Rôle : Effectuer plusieurs micro-réflexions internes avant de produire une réponse finale
Priorité : 3 (après perception et avant LLM)
Auteur : Matthieu & GPT
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cycle_interne")

class CycleInternePlugin(BasePlugin):
    meta = Meta(
        name="cycle_interne",
        priority=3,
        version="1.2",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    ANGLES = [
        "stratégique", "fonctionnel", "expérientiel",
        "émotionnel", "logique", "systémique",
        "éthique", "symbolique", "technique"
    ]

    def micro_reflexion(self, objectif: str, index: int) -> str:
        angle = random.choice(self.ANGLES)
        amorce = random.choice([
            "Je me demande si",
            "Il serait intéressant d'examiner si",
            "Je perçois une ouverture via",
            "Une piste à explorer serait",
            "Peut-on envisager",
            "Je soupçonne que"
        ])
        return f"Étape {index} ({angle}) : {amorce} « {objectif} » sous l'angle {angle.lower()}."

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif_raw = ctx.get("objectif", "")
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", "")).strip()
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw.strip()
        else:
            objectif = str(objectif_raw).strip()

        if not objectif:
            plugins_log.append("CycleInternePlugin : 🚫 Aucun objectif à raisonner.")
            logger.info("[cycle_interne] Aucun objectif présent, réflexion interne annulée.")
            return ctx

        # Générer 3 micro-réflexions
        etapes = [self.micro_reflexion(objectif, i) for i in range(1, 4)]

        synthese = (
            "🧩 Je vais traiter cet objectif par plusieurs micro-réflexions internes :\n"
            + "\n".join(f"→ {e}" for e in etapes) + "\n"
            + "Cela devrait me permettre d'accéder à une réponse plus cohérente et multidimensionnelle."
        )

        ctx["reflexion_interne_etapes"] = etapes
        ctx["reflexion_interne"] = synthese
        plugins_log.append("CycleInternePlugin : 🌀 réflexion interne multiphase effectuée.")
        logger.info(f"[cycle_interne] Réflexion interne générée avec {len(etapes)} étapes.")

        return ctx
