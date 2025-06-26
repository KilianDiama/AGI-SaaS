# plugins/plugin_tendance_adaptative.py

import os
import json
import re
from collections import Counter
from noyau_core import BasePlugin, Context, Meta

MEMORY_FILE = "./data/memoire_narrative.json"

class PluginTendanceAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_tendance_adaptative",
        version="1.0",
        priority=2.6,
        author="Toi & GPT"
    )

    def _extraire_tendances(self, introspections):
        erreurs = []
        réussites = []
        remarques = []

        for entry in introspections:
            texte = entry.lower()
            if "erreur" in texte or "échec" in texte:
                erreurs.append(texte)
            elif "réussi" in texte or "pertinent" in texte or "logique" in texte:
                réussites.append(texte)
            else:
                remarques.append(texte)

        top_erreurs = Counter([self._simplifier(e) for e in erreurs]).most_common(5)
        top_reussites = Counter([self._simplifier(r) for r in réussites]).most_common(5)

        return {
            "top_erreurs": top_erreurs,
            "top_reussites": top_reussites,
            "nb_total": len(introspections)
        }

    def _simplifier(self, phrase):
        phrase = re.sub(r"[^a-zA-ZÀ-ÿ\s]", "", phrase)
        return " ".join(phrase.strip().split()[:7])  # simplifie par les 7 premiers mots

    async def run(self, ctx: Context) -> Context:
        if not os.path.exists(MEMORY_FILE):
            ctx["tendance_adaptative"] = {
                "msg": "Pas encore assez d’introspection pour analyser les tendances."
            }
            return ctx

        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)

            tendances = self._extraire_tendances(data[-100:])
            ctx["tendance_adaptative"] = tendances
            ctx.setdefault("plugins_log", []).append("PluginTendanceAdaptative : tendances détectées.")
        except Exception as e:
            ctx["tendance_adaptative"] = {
                "msg": f"Erreur d’analyse des tendances : {str(e)}"
            }

        return ctx
