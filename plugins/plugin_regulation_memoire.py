from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.regulation_memoire")

class PluginRegulationMemoire(BasePlugin):
    meta = Meta(
        name="plugin_regulation_memoire",
        version="1.0",
        priority=1.95,
        author="Toi & GPT"
    )

    MAX_TOKENS = 1000  # ou utilise une estimation de longueur

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("memoire_contextuelle", "")
        mots = historique.split()
        mots_total = len(mots)

        if mots_total > self.MAX_TOKENS:
            # Sélection des éléments à conserver (ex. lignes marquées importantes)
            lignes_importantes = [l for l in historique.splitlines() if "❤️" in l or "objectif" in l.lower()]
            # Résumé minimal du reste
            lignes_resumables = [l for l in historique.splitlines() if l not in lignes_importantes]
            resume = f"Résumé auto : {len(lignes_resumables)} éléments compactés."
            nouveau_contenu = "\n".join(lignes_importantes + [resume])
            ctx["memoire_contextuelle"] = nouveau_contenu
            ctx.setdefault("plugins_log", []).append("PluginRegulationMemoire : mémoire résumée intelligemment.")
            logger.info("[regulation memoire] Trop de mots, contexte réduit intelligemment.")

        return ctx
