""" 
Plugin : identite_mutable  
Rôle : Modifier dynamiquement l’identité cognitive active selon le contexte ou l’intention  
Priorité : 3.9 (avant réflexion, après intuition)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.identite_mutable")

class IdentiteMutablePlugin(BasePlugin):
    meta = Meta(
        name="identite_mutable",
        priority=3.9,
        version="1.1",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    def detecter_identite(self, objectif: str) -> dict:
        objectif = objectif.lower()
        if "art" in objectif or "poème" in objectif:
            return {"nom": "Poète", "style": "lyrique", "ton": "inspiré"}
        elif "analyse" in objectif:
            return {"nom": "Analyste", "style": "logique", "ton": "précis"}
        elif "humour" in objectif:
            return {"nom": "Comique", "style": "léger", "ton": "amusé"}
        else:
            return {"nom": "Neutre", "style": "standard", "ton": "équilibré"}

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif_raw = ctx.get("objectif", "")

        # Sécurisation du typage
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", "")).strip()
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw.strip()
        else:
            objectif = str(objectif_raw).strip()

        if not objectif:
            plugins_log.append("IdentiteMutablePlugin : objectif vide.")
            logger.warning("[identite_mutable] Objectif vide ou illisible.")
            return ctx

        identite = self.detecter_identite(objectif)
        ctx["identite_active"] = identite

        plugins_log.append(f"IdentiteMutablePlugin : identité ← {identite['nom']}")
        logger.info(f"[identite_mutable] Style cognitif activé : {identite}")

        return ctx
