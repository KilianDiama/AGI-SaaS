# plugins/plugin_objet_connaissance.py

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.objet_connaissance")

class PluginObjetConnaissance(BasePlugin):
    meta = Meta(
        name="plugin_objet_connaissance",
        priority=3.9,
        version="1.0",
        author="Toi & GPT"
    )

    def __init__(self):
        self.nom = "plugin_objet_connaissance"

    async def run(self, ctx: Context) -> Context:
        mémoire = ctx.setdefault("objets_connaissance", {})
        texte = (ctx.get("llm_response", "") + " " + ctx.get("llm_prompt", "")).strip()
        objets = self._extraire_objets_potentiels(texte)

        for objet in objets:
            now = datetime.utcnow().isoformat()
            if objet not in mémoire:
                mémoire[objet] = {
                    "première_mention": now,
                    "dernière_mention": now,
                    "contexte": [texte],
                    "comptage": 1
                }
            else:
                mémoire[objet]["dernière_mention"] = now
                mémoire[objet]["contexte"].append(texte)
                mémoire[objet]["comptage"] += 1

        logger.info(f"[{self.nom}] Objets mis à jour : {list(objets)}")
        ctx["objets_connaissance"] = mémoire
        ctx.setdefault("plugins_log", []).append(f"{self.nom} : {len(objets)} objets détectés")

        return ctx

    def _extraire_objets_potentiels(self, texte: str) -> set:
        import re

        candidats = set()
        mots = re.findall(r"\b[a-z]{5,}\b", texte)  # mots de plus de 4 lettres, minuscules

        exclusions = {"https", "http", "mailto", "about", "plugin", "fonction", "objectifs"}  # filtrage brut
        for mot in mots:
            if mot not in exclusions:
                candidats.add(mot)

        return candidats
