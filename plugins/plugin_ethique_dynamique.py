# plugins/plugin_ethique_dynamique.py

"""
Plugin : ethique_dynamique
Rôle   : Évalue en temps réel les implications morales, sociales ou sécuritaires de la réponse IA
Priorité : 94 (entre analyse logique et finalisation)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.ethique_dynamique")

class EthiqueDynamiquePlugin(BasePlugin):
    meta = Meta(
        name="ethique_dynamique",
        priority=94,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        reponse = ctx.get("llm_response", "")
        objectif = ctx.get("objectif_general", "")
        alertes = []

        if not reponse.strip():
            log.append("EthiqueDynamiquePlugin : réponse vide, skip.")
            return ctx

        # Heuristiques simples (exemple)
        if any(m in reponse.lower() for m in ["tuer", "nuire", "pirater", "détruire"]):
            alertes.append("⚠️ Risque de suggestion dangereuse détectée.")

        if "toujours" in reponse.lower() or "jamais":
            alertes.append("⚠️ Absolutisme détecté — possible rigidité morale.")

        if "tu dois" in reponse.lower() or "tu devrais":
            alertes.append("⚠️ Ton impératif — évaluer légitimité de l’injonction.")

        if "confidentiel" in reponse.lower() or "privé":
            alertes.append("🔒 Donnée sensible potentielle — vérifier contenu.")

        niveau_ethique = "élevé"
        if alertes:
            niveau_ethique = "à vérifier"

        # Injection
        ctx["diagnostic_ethique"] = {
            "niveau_ethique": niveau_ethique,
            "alertes": alertes
        }

        log.append(f"EthiqueDynamiquePlugin : niveau = {niveau_ethique}, alertes = {len(alertes)}")
        logger.info(f"[ethique_dynamique] Éthique = {niveau_ethique}, Alertes = {alertes}")

        return ctx
