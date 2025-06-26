"""
Plugin : auto_debug
Rôle : Relecture et diagnostic d'ambiguïtés ou erreurs potentielles dans la réponse générée
Priorité : 6 (après validation logique)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.auto_debug")

class AutoDebugPlugin(BasePlugin):
    meta = Meta(
        name="auto_debug",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        response = ctx.get("llm_response", "")

        if not response.strip():
            ctx["auto_debug"] = "❌ Aucune réponse à diagnostiquer."
            plugins_log.append("AutoDebugPlugin : réponse vide")
            return ctx

        remarques = []

        # Trop de répétitions ?
        mots = response.lower().split()
        freq = {mot: mots.count(mot) for mot in set(mots)}
        doublons = [mot for mot, count in freq.items() if count > 5 and len(mot) > 3]
        if doublons:
            remarques.append(f"🔁 Répétitions excessives : {', '.join(doublons)}")

        # Formulations douteuses
        if "peut-être que je ne suis pas sûr" in response.lower():
            remarques.append("⚠️ Formulation floue ou contradictoire détectée.")

        # Longueur extrême
        if len(response) > 1500:
            remarques.append("📏 Réponse très longue : possible verbiage ou perte de clarté.")

        # Vérification simple de compréhension
        if "je ne comprends pas" in response.lower() or "je ne suis pas sûr" in response.lower():
            remarques.append("🧩 Manque de clarté ou de compréhension affirmé dans la réponse.")

        # Analyse de syntaxe simple
        phrases = re.split(r'[.!?]', response)
        phrases_courtes = [p for p in phrases if len(p.strip().split()) <= 3]
        if len(phrases_courtes) > 5:
            remarques.append("🪓 Beaucoup de phrases très courtes : style haché ?")

        ctx["auto_debug"] = "\n".join(remarques) if remarques else "🟢 Aucun problème détecté dans la sortie."
        plugins_log.append("AutoDebugPlugin : diagnostic réalisé")
        logger.info("[auto_debug] Debug terminé")

        return ctx
