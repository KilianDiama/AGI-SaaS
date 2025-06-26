""" 
Plugin : navigation_spatiale  
Rôle : Cartographier les concepts en un graphe mental (topologie cognitive)  
Priorité : 5.8 (entre analyse et création)  
Auteur : Matthieu & GPT  
"""

import logging
from hashlib import sha1
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.navigation_spatiale")

class NavigationSpatialePlugin(BasePlugin):
    meta = Meta(
        name="navigation_spatiale",
        priority=5.8,
        version="1.1",  # version corrigée
        author="Matthieu & GPT"
    )

    def generer_id(self, texte) -> str:
        texte_str = str(texte)
        return sha1(texte_str.encode("utf-8")).hexdigest()[:8]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        elements = {
            "objectif": ctx.get("objectif", ""),
            "reponse": ctx.get("response", ""),
            "idee": ctx.get("idee_emergente", "")
        }

        graphe = []
        for nom, contenu in elements.items():
            if not contenu:
                continue
            contenu_str = str(contenu)  # Sécurité type
            noeud_id = self.generer_id(contenu_str)
            graphe.append({
                "id": noeud_id,
                "label": nom,
                "contenu": contenu_str[:120],
                "liens": [e for e in elements if e != nom]
            })

        ctx["graphe_conceptuel"] = graphe
        plugins_log.append("NavigationSpatialePlugin : graphe conceptuel généré.")
        logger.info("[navigation_spatiale] Graphe mental formé.")

        return ctx
