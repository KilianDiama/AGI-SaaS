""" 
Plugin : reseau_idees  
Rôle : Construire un graphe persistant des idées et relations entre concepts internes  
Priorité : 5.6 (après emergence, avant création artistique)  
Auteur : Matthieu & GPT  
"""

import logging
import os
import json
from hashlib import sha1
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reseau_idees")

class ReseauIdeesPlugin(BasePlugin):
    meta = Meta(
        name="reseau_idees",
        priority=5.6,
        version="1.1",  # version corrigée
        author="Matthieu & GPT"
    )

    RESEAU_PATH = "data/reseau_idees.json"

    def charger_reseau(self):
        if os.path.exists(self.RESEAU_PATH):
            with open(self.RESEAU_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def enregistrer_reseau(self, reseau):
        with open(self.RESEAU_PATH, "w", encoding="utf-8") as f:
            json.dump(reseau, f, ensure_ascii=False, indent=2)

    def generer_id(self, texte) -> str:
        # S'assurer que le texte est bien une chaîne encodable
        texte_str = str(texte)
        return sha1(texte_str.encode("utf-8")).hexdigest()[:10]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        reseau = self.charger_reseau()

        sources = {
            "objectif": ctx.get("objectif", ""),
            "idee": ctx.get("idee_emergente", ""),
            "plan": ctx.get("plan_autonome", ""),
            "projection": ctx.get("projection_futuriste", "")
        }

        nouveaux = {}
        for cle, val in sources.items():
            if val:
                val_str = str(val)  # Sécurité typage
                _id = self.generer_id(val_str)
                nouveaux[_id] = {
                    "label": cle,
                    "contenu": val_str[:120],
                    "liens": []
                }

        for id1 in nouveaux:
            for id2 in nouveaux:
                if id1 != id2 and id2 not in nouveaux[id1]["liens"]:
                    nouveaux[id1]["liens"].append(id2)

        for nid, node in nouveaux.items():
            if nid not in reseau:
                reseau[nid] = node
            else:
                reseau[nid]["liens"] = list(set(reseau[nid]["liens"] + node["liens"]))

        ctx["reseau_idees"] = nouveaux
        self.enregistrer_reseau(reseau)

        plugins_log.append("ReseauIdeesPlugin : graphe cognitif étendu.")
        logger.info("[reseau_idees] Hypergraphe cognitif mis à jour.")

        return ctx
