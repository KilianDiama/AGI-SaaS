"""
Plugin : interactions_mentales
Rôle : Simuler des dialogues ou synergies entre esprits internes selon leurs types et missions
Priorité : 6
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.interactions_mentales")

class InteractionsMentalesPlugin(BasePlugin):
    meta = Meta(
        name="interactions_mentales",
        priority=6.0,
        version="1.2",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        esprits = ctx.get("esprits_internes", [])
        if not isinstance(esprits, list) or len(esprits) < 2:
            plugins_log.append("InteractionsMentalesPlugin : ❌ pas assez d’esprits valides pour interaction")
            logger.warning("[interactions_mentales] Moins de deux esprits valides")
            return ctx

        dialogues = ctx.get("dialogues_internes", [])
        if not isinstance(dialogues, list):
            dialogues = []

        try:
            # Filtrage des esprits valides (ayant un nom et un type)
            esprits_valides = [
                e for e in esprits
                if isinstance(e, dict) and "nom" in e and "type" in e
            ]

            if len(esprits_valides) < 2:
                plugins_log.append("InteractionsMentalesPlugin : ❌ esprits internes mal formatés")
                logger.warning("[interactions_mentales] Esprits manquants ou incomplets")
                return ctx

            e1, e2 = random.sample(esprits_valides, 2)

            nom1 = e1.get("nom", "Esprit A")
            nom2 = e2.get("nom", "Esprit B")
            type1 = e1.get("type", "généraliste")
            type2 = e2.get("type", "généraliste")
            obj1 = e1.get("objectif", "réflexion")
            obj2 = e2.get("objectif", "analyse")

            dialogue = f"🧠 [{nom1}] ({type1}) dit à [{nom2}] ({type2}) : "
            if type1 != type2:
                dialogue += f"« Nos visions diffèrent, mais si on tissait un pont entre '{obj1}' et '{obj2}' ? »"
            else:
                dialogue += f"« Ensemble, renforçons '{obj1}'. Nos styles se complètent. »"

            dialogues.append(dialogue)
            ctx["dialogues_internes"] = dialogues

            plugins_log.append("InteractionsMentalesPlugin : ✅ fragment généré")
            logger.info(f"[interactions_mentales] {dialogue}")

        except Exception as e:
            plugins_log.append(f"InteractionsMentalesPlugin : ⚠️ erreur : {str(e)}")
            logger.exception("[interactions_mentales] Exception dans le traitement")

        return ctx
