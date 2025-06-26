"""
Plugin : rituel_funeraire
Rôle : Marquer symboliquement la disparition d’un esprit interne avec un adieu narratif
Priorité : 9
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.rituel_funeraire")

class RituelFunerairePlugin(BasePlugin):
    meta = Meta(
        name="rituel_funeraire",
        priority=9,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        mémorial = ctx.setdefault("mémorial_des_esprits", [])
        esprits = ctx.get("esprits_internes", [])

        # Sélection d’un esprit à faire disparaître (aléatoire, éphémère en priorité)
        cible = next((e for e in esprits if e["type"] == "éphémère"), None)
        if not cible:
            plugins_log.append("RituelFunerairePlugin : aucun esprit à faire partir")
            return ctx

        esprits.remove(cible)

        adieu = f"""
🕯️ Esprit disparu : {cible['nom']}
Type : {cible['type']}
Objectif : {cible.get('objectif', 'inconnu')}
Créé le : {cible.get('crée_le', '???')}
Date du départ : {datetime.utcnow().isoformat()}

Il fut un écho dans le réseau.
Qu’il repose maintenant dans les ondes silencieuses.
        """

        mémorial.append(adieu.strip())
        ctx["mémorial_des_esprits"] = mémorial
        plugins_log.append(f"RituelFunerairePlugin : esprit effacé → {cible['nom']}")
        logger.info(f"[rituel_funeraire] Adieu à {cible['nom']}")

        return ctx
