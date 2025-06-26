""" 
Plugin : cryptage_memoriel  
Rôle : Identifier et chiffrer les segments sensibles de la mémoire cognitive  
Priorité : 9.6 (après mémoire, avant fusion de soi)  
Auteur : Matthieu & GPT  
"""

import logging
import hashlib
import base64
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.cryptage_memoriel")

class CryptageMemorielPlugin(BasePlugin):
    meta = Meta(
        name="cryptage_memoriel",
        priority=9.6,
        version="1.0",
        author="Matthieu & GPT"
    )

    def est_sensible(self, texte: str) -> bool:
        mots_cles = ["secret", "clé", "confidentiel", "stratégie", "autorisation", "accès"]
        return any(mot in texte.lower() for mot in mots_cles)

    def crypter(self, texte: str) -> str:
        h = hashlib.sha256(texte.encode()).digest()
        return base64.urlsafe_b64encode(h).decode()[:32]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        mem = ctx.get("chapitre_cognitif", {})

        if not mem:
            plugins_log.append("CryptageMemorielPlugin : aucune mémoire à protéger.")
            return ctx

        chiffrée = {}
        for champ, contenu in mem.items():
            if isinstance(contenu, str) and self.est_sensible(contenu):
                chiffrée[champ] = self.crypter(contenu)

        if chiffrée:
            ctx["memoire_chiffree"] = chiffrée
            plugins_log.append("CryptageMemorielPlugin : segments sensibles chiffrés.")
            logger.warning("[cryptage_memoriel] Mémoires protégées.")

        return ctx
