import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.synthese_active")

class PluginSyntheseActive(BasePlugin):
    meta = Meta(
        name="plugin_synthese_active",
        version="1.0",
        priority=2.5,  # Après raisonnement, avant génération finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("historique", [])
        if not historique:
            logger.info("[synthese_active] Aucun historique pour synthèse.")
            ctx.setdefault("plugins_log", []).append("PluginSyntheseActive : historique vide")
            return ctx

        messages = [item["message"] for item in historique if item["from"] == "user"]
        if not messages:
            logger.info("[synthese_active] Aucun message utilisateur trouvé.")
            return ctx

        texte = "\n".join(messages[-5:])  # On prend les derniers échanges
        résumé = await self._resumer(texte)

        ctx["synthese_active"] = résumé
        ctx.setdefault("plugins_log", []).append("PluginSyntheseActive : résumé actif généré")
        logger.info(f"[synthese_active] Résumé actif : {résumé}")
        return ctx

    async def _resumer(self, texte: str) -> str:
        # Implémentation simplifiée, on pourrait ici appeler un LLM ou un module natif
        lignes = texte.strip().split("\n")
        if len(lignes) <= 2:
            return "Interaction courte, résumé inutile."
        return f"Résumé des derniers échanges : {lignes[0][:60]}... → {lignes[-1][:60]}..."

