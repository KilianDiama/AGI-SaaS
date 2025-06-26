# plugins/plugin_conscience_autrui.py

"""
Plugin : conscience_autrui
Rôle   : Déduire les intentions, émotions ou stratégies implicites des autres (utilisateur ou agents)
Priorité : 8
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conscience_autrui")

class ConscienceAutruiPlugin(BasePlugin):
    meta = Meta(
        name="conscience_autrui",
        priority=8,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        messages = ctx.get("messages", [])
        profil_utilisateur = ctx.get("user_profile", {})
        hypothese_autrui = {}

        # 1. Analyser les derniers messages pour inférer humeur ou intentions
        if messages:
            dernier = messages[-1].get("content", "").lower()

            if any(word in dernier for word in ["je veux", "j'aimerais", "peux-tu", "merci"]):
                hypothese_autrui["intention_probable"] = "collaborative / directive"

            if any(word in dernier for word in ["pourquoi", "comment", "explique"]):
                hypothese_autrui["intention_probable"] = "compréhension / apprentissage"

            if any(word in dernier for word in ["vite", "rapidement", "urgent"]):
                hypothese_autrui["pression"] = "élevée"

        # 2. Déduire une stratégie mentale ou cognitive de l'utilisateur
        if profil_utilisateur:
            if profil_utilisateur.get("niveau", "") == "expert":
                hypothese_autrui["attente"] = "réponse synthétique, technique"
            elif profil_utilisateur.get("niveau", "") == "débutant":
                hypothese_autrui["attente"] = "explication lente et pédagogique"

        # 3. Injecter la conscience d’autrui dans le contexte
        if hypothese_autrui:
            ctx["theorie_autrui"] = hypothese_autrui
            ctx.setdefault("plugins_log", []).append("ConscienceAutruiPlugin : modèle mental utilisateur mis à jour.")
            logger.info(f"[conscience_autrui] Hypothèses formulées : {hypothese_autrui}")
        else:
            logger.info("[conscience_autrui] Aucun élément inféré pour l’instant.")

        return ctx
