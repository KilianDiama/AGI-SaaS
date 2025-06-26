"""
Plugin : memoire_transversale
Rôle : Créer des liens entre souvenirs dispersés ou isolés, selon leur similarité contextuelle
Priorité : 2 (après récupération mémoire)
Auteur : GPT pour AGI_X
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.memoire_transversale")

class MemoireTransversalePlugin(BasePlugin):
    meta = Meta(
        name="memoire_transversale",
        priority=2,
        version="1.0",
        author="GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        souvenirs = ctx.get("memoire", {}).get("long_terme", [])

        if not souvenirs or len(souvenirs) < 3:
            ctx["memoire_transversale"] = "⚠️ Trop peu de souvenirs pour créer des connexions utiles."
            plugins_log.append("MemoireTransversalePlugin : mémoire insuffisante")
            return ctx

        liens = []
        for i in range(len(souvenirs)):
            for j in range(i + 1, len(souvenirs)):
                a, b = souvenirs[i], souvenirs[j]
                if a and b and any(word in a and word in b for word in ["objectif", "erreur", "réussite", "utilisateur", "conflit"]):
                    liens.append((a[:40], b[:40]))

        if liens:
            resultats = [f"• Lien détecté entre : «{a}...» et «{b}...»" for a, b in liens[:5]]
            ctx["memoire_transversale"] = "\n".join(resultats)
            plugins_log.append(f"MemoireTransversalePlugin : {len(liens)} connexions créées")
        else:
            ctx["memoire_transversale"] = "🌀 Aucun lien évident trouvé entre souvenirs."
            plugins_log.append("MemoireTransversalePlugin : aucun lien trouvé")

        logger.info("[memoire_transversale] Connexions établies")

        return ctx
