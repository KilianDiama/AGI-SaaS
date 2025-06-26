"""
Plugin : paradoxe_heberge
Rôle : Permettre l’hébergement de pensées ou logiques contradictoires sans résolution forcée
Priorité : 4
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.paradoxe_heberge")

class ParadoxeHébergéPlugin(BasePlugin):
    meta = Meta(
        name="paradoxe_heberge",
        priority=4,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        paradoxe = ctx.setdefault("paradoxes", [])

        # Exemples de zones à contradictions possibles
        logique = ctx.get("validation_logique", "")
        intuition = ctx.get("reflexion_interne", "")
        mémoire = ctx.get("souvenirs_recent", "")

        contradictions = []

        if "faux" in logique.lower() and "je pense que" in intuition.lower():
            contradictions.append("💭 Intuition en tension avec logique")

        if "cohérent" in logique.lower() and "contradiction" in mémoire.lower():
            contradictions.append("🧠 Souvenir paradoxal à l’analyse actuelle")

        if contradictions:
            paradoxe.append({
                "cycle": len(ctx.get("souffle_narratif", [])),
                "contradictions": contradictions
            })
            ctx["paradoxes"] = paradoxe
            plugins_log.append("ParadoxeHébergéPlugin : contradiction acceptée")
            logger.info(f"[paradoxe_heberge] Contradictions hébergées : {contradictions}")
        else:
            plugins_log.append("ParadoxeHébergéPlugin : aucun paradoxe relevé")

        return ctx
