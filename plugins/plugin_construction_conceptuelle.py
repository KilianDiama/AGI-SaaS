# plugins/plugin_construction_conceptuelle.py

"""
Plugin : construction_conceptuelle
Rôle   : Crée de nouveaux concepts ou abstractions à partir des patterns traversés dans les raisonnements récents
Priorité : 97 (avant final_synthesis)
Auteur  : Toi + GPT
"""

import logging
import hashlib
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.construction_conceptuelle")

class ConstructionConceptuellePlugin(BasePlugin):
    meta = Meta(
        name="construction_conceptuelle",
        priority=97,
        version="1.0",
        author="Toi + GPT"
    )

    memoire_concepts = {}

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        concepts_detectés = ctx.get("emergence_logique", [])
        objections = ctx.get("contre_arguments", [])
        objectif = ctx.get("objectif_general", "")
        synthese_brute = objectif + " " + " ".join(concepts_detectés + objections)

        if len(synthese_brute.strip()) < 30:
            log.append("ConstructionConceptuellePlugin : contenu insuffisant pour abstraction.")
            return ctx

        # Génère un nom de concept à partir d’un hash partiel
        hash_id = hashlib.sha1(synthese_brute.encode()).hexdigest()[:8]
        nom_concept = f"concept_{hash_id}"

        if nom_concept in self.memoire_concepts:
            log.append(f"ConstructionConceptuellePlugin : concept déjà existant ({nom_concept})")
            return ctx

        nouveau_concept = {
            "nom": nom_concept,
            "base": synthese_brute,
            "origine": ctx.get("cycle_id"),
            "tags": concepts_detectés[:3] + objections[:3],
        }

        self.memoire_concepts[nom_concept] = nouveau_concept
        ctx.setdefault("concepts_crees", []).append(nouveau_concept)
        log.append(f"ConstructionConceptuellePlugin : concept abstrait généré : {nom_concept}")
        logger.info(f"[construction_conceptuelle] Nouveau concept synthétisé : {nom_concept}")

        return ctx
