# plugins/plugin_contre_arguments.py

"""
Plugin : contre_arguments
Rôle   : Produit des contre-arguments à sa propre réponse pour valider, renforcer ou corriger sa logique
Priorité : 90 (juste avant la synthèse finale)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.contre_arguments")

class ContreArgumentsPlugin(BasePlugin):
    meta = Meta(
        name="contre_arguments",
        priority=90,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        demande = ctx.get("message", "")
        contre_arguments = []

        if not reponse or len(reponse) < 10:
            log.append("ContreArgumentsPlugin : réponse trop courte, skip.")
            return ctx

        # Heuristique simple pour générer un contre-argument simulé
        if any(mot in reponse.lower() for mot in ["toujours", "jamais", "impossible"]):
            contre_arguments.append("La réponse utilise des absolus qui peuvent être discutables.")

        if "car" in reponse and "mais" not in reponse:
            contre_arguments.append("Il manque peut-être un point de vue contradictoire.")

        if demande.lower().startswith("pourquoi"):
            contre_arguments.append("Une alternative causale pourrait exister.")

        # Résultat final
        if contre_arguments:
            ctx["contre_arguments"] = contre_arguments
            log.append(f"ContreArgumentsPlugin : {len(contre_arguments)} objections générées.")
            logger.info(f"[contre_arguments] Objections : {contre_arguments}")
        else:
            log.append("ContreArgumentsPlugin : aucune objection détectée.")

        return ctx
