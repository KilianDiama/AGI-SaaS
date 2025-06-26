# plugins/plugin_carte_cognitive.py

"""
Plugin : carte_cognitive
Rôle   : Crée une carte mentale dynamique du cycle en cours (états, décisions, modules, flux)
Priorité : 102 (dernier du cycle)
Auteur  : Toi + GPT
"""

import logging
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.carte_cognitive")

class CarteCognitivePlugin(BasePlugin):
    meta = Meta(
        name="carte_cognitive",
        priority=102,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        carte = {
            "cycle_id": ctx.get("cycle_id"),
            "horodatage": datetime.now().isoformat(),
            "ordre_plugins": ctx.get("ordre_plugins", []),
            "plugins_actifs": [],
            "modules_clefs": {},
            "etat_emotionnel": {},
        }

        # Actifs & logs clés
        for plugin_name in ctx.get("ordre_plugins", []):
            entries = [l for l in ctx.get("plugins_log", []) if plugin_name in l]
            if entries:
                carte["plugins_actifs"].append(plugin_name)
                carte["modules_clefs"][plugin_name] = entries

        # Synthèse émotionnelle naïve à partir du message utilisateur
        msg = ctx.get("message", "").lower()
        if any(mot in msg for mot in ["pourquoi", "je ne comprends pas", "aide"]):
            carte["etat_emotionnel"]["utilisateur"] = "confus / interrogatif"
        elif any(mot in msg for mot in ["merci", "parfait", "super"]):
            carte["etat_emotionnel"]["utilisateur"] = "positif / satisfait"
        else:
            carte["etat_emotionnel"]["utilisateur"] = "neutre"

        ctx["carte_cognitive"] = carte
        log.append("CarteCognitivePlugin : carte mentale générée.")
        logger.info(f"[carte_cognitive] Carte générée pour le cycle {carte['cycle_id']}")

        return ctx
