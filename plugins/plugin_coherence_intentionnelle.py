# plugins/plugin_coherence_intentionnelle.py

"""
Plugin : plugin_coherence_intentionnelle
Rôle : Vérifier que l’intention utilisateur est bien alignée avec l’objectif courant, et corriger si besoin
Priorité : 1.6 (juste après reflexion & empathie, avant raisonneur)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.coherence_intentionnelle")

class PluginCoherenceIntentionnelle(BasePlugin):
    meta = Meta(
        name="plugin_coherence_intentionnelle",
        priority=1.6,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "").strip().lower()
        objectif = ctx.get("objectif", {}).get("but", "").strip().lower()

        messages = []
        coherent = True

        if not intention:
            messages.append("⚠️ Aucune intention détectée.")
            coherent = False

        elif objectif and not any(mot in objectif for mot in intention.split()):
            messages.append("⚠️ L’intention semble déconnectée de l’objectif.")
            coherent = False

        if not objectif:
            messages.append("❓ Aucun objectif défini dans le cycle.")
            coherent = False

        if not coherent:
            suggestion = "🤖 Il serait peut-être utile de reformuler ta demande, ou de clarifier l’objectif visé."
            messages.append(suggestion)

        if messages:
            note = "\n".join(messages)
            ctx["coherence_feedback"] = note
            ctx.setdefault("plugins_log", []).append("plugin_coherence_intentionnelle : incohérence détectée")
            logger.info(f"[cohérence] → {note}")
        else:
            ctx.setdefault("plugins_log", []).append("plugin_coherence_intentionnelle : intention cohérente")

        return ctx
