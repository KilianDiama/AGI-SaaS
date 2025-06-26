""" 
Plugin : instanciation_multiple  
Rôle : Créer des sous-instances mentales spécialisées de l’AGI principale  
Priorité : 7.8 (juste après dialectique et synthèse cognitive)  
Auteur : Matthieu & GPT  
"""

import logging
from copy import deepcopy
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.instanciation_multiple")

class InstanciationMultiplePlugin(BasePlugin):
    meta = Meta(
        name="instanciation_multiple",
        priority=7.8,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        roles = ["analyste", "créatif", "critique", "historien", "philosophe"]
        sous_instances = {}

        for role in roles:
            clone = deepcopy(ctx)
            clone["nom_instance"] = f"{ctx.get('nom_systeme', 'Instance')}::{role}"
            clone["objectif"] = f"[Rôle {role}] : {ctx.get('objectif', '')}"
            sous_instances[role] = clone

        ctx["sous_instance"] = sous_instances
        plugins_log.append(f"InstanciationMultiplePlugin : {len(roles)} sous-instances créées.")
        logger.info("[instanciation_multiple] Multiples rôles cognitifs instanciés.")

        return ctx
