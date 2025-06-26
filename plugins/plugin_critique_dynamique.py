# plugins/plugin_critique_dynamique.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.critique_dynamique")

class PluginCritiqueDynamique(BasePlugin):
    meta = Meta(
        name="plugin_critique_dynamique",
        version="1.0",
        priority=3.6,  # Juste après le raisonneur
        author="Toi & GPT"
    )

    def __init__(self):
        self.critiqueurs = {
            "modérateur": self.avis_moderateur,
            "critique": self.avis_critique,
            "expert": self.avis_expert,
            "utilisateur_simulé": self.avis_utilisateur
        }

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("response", "").strip()
        if not texte:
            ctx.setdefault("plugins_log", []).append("PluginCritiqueDynamique : pas de réponse à analyser.")
            return ctx

        resultat = self.evaluer(texte)
        ctx["dynamic_critique"] = resultat

        if resultat["doit_reformuler"]:
            ctx["response"] = resultat["reformulation"]
            ctx.setdefault("plugins_log", []).append("PluginCritiqueDynamique : réponse reformulée 🔁")
        else:
            ctx.setdefault("plugins_log", []).append("PluginCritiqueDynamique : réponse jugée satisfaisante ✅")

        logger.info(f"[CritiqueDynamique] Analyse multi-rôle : {resultat['analyses']}")
        return ctx

    def evaluer(self, réponse: str) -> dict:
        analyses = {rôle: fn(réponse) for rôle, fn in self.critiqueurs.items()}
        besoins_amélioration = [rôle for rôle, analyse in analyses.items() if analyse["améliorer"]]

        nouvelle_version = self.reformuler(réponse, analyses) if besoins_amélioration else réponse

        return {
            "analyses": analyses,
            "reformulation": nouvelle_version,
            "doit_reformuler": bool(besoins_amélioration)
        }

    def avis_moderateur(self, texte):
        if len(texte) < 80:
            return {"avis": "Réponse trop courte.", "améliorer": True}
        return {"avis": "Longueur adéquate.", "améliorer": False}

    def avis_critique(self, texte):
        if "exception" in texte.lower():
            return {"avis": "Langage technique non justifié pour l'utilisateur.", "améliorer": True}
        return {"avis": "Ton global cohérent.", "améliorer": False}

    def avis_expert(self, texte):
        if "je sais pas" in texte.lower():
            return {"avis": "Manque de précision ou expertise.", "améliorer": True}
        return {"avis": "Réponse techniquement crédible.", "améliorer": False}

    def avis_utilisateur(self, texte):
        if "..." in texte or texte.endswith(":"):
            return {"avis": "Réponse incomplète perçue par un humain.", "améliorer": True}
        return {"avis": "Compréhensible pour un utilisateur.", "améliorer": False}

    def reformuler(self, texte, analyses):
        instructions = [analyse["avis"] for analyse in analyses.values() if analyse["améliorer"]]
        commentaire = " | ".join(instructions)
        return f"🛠️ Révision automatique :\n{texte}\n\n🔁 Ajustements suggérés : {commentaire}"
