"""
Plugin : reflexion_miroir
Rôle : Comparer deux cycles internes pour analyser l’évolution de soi
Priorité : 24
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.reflexion_miroir")

class ReflexionMiroirPlugin(BasePlugin):
    meta = Meta(
        name="reflexion_miroir",
        priority=24,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        archive = ctx.get("feedback_archive", [])
        plugins_log = ctx.setdefault("plugins_log", [])

        if len(archive) < 2:
            ctx["reflexion_miroir"] = "📭 Pas assez de cycles enregistrés pour faire un miroir."
            return ctx

        cycle_1 = archive[-2]
        cycle_2 = archive[-1]

        comparaison = [
            "🪞 **Réflexion Miroir**",
            "",
            f"📅 Cycle {len(archive)-1} → {cycle_1['date']}",
            f"🗨 Réponse : {cycle_1['réponse'][:60]}...",
            f"💬 Critique : {cycle_1['critique'][:40]}",
            "",
            f"📅 Cycle {len(archive)} → {cycle_2['date']}",
            f"🗨 Réponse : {cycle_2['réponse'][:60]}...",
            f"💬 Critique : {cycle_2['critique'][:40]}",
            "",
            "🔍 **Analyse** :",
            "– Y a-t-il plus de confiance, ou plus de prudence ?",
            "– Le style devient-il plus fluide ?",
            "– Les doutes se répètent-ils ou évoluent-ils ?",
            "",
            "🧠 Que veux-tu retenir de ce miroir ?"
        ]

        ctx["reflexion_miroir"] = "\n".join(comparaison)
        plugins_log.append("ReflexionMiroirPlugin : comparaison effectuée")
        logger.info("[reflexion_miroir] Deux cycles comparés")

        return ctx
