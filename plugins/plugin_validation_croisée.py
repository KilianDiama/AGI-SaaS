import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.validation_croisée")

class PluginValidationCroisée(BasePlugin):
    meta = Meta(
        name="plugin_validation_croisée",
        version="1.0",
        priority=3.2,  # Avant le vote et fusion, après génération logique
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        raisonnement = ctx.get("response_logique", "").strip()
        analyse = ctx.get("analysis_feedback", "").strip()
        reflexion = ctx.get("reflexion_interne", "").strip()
        memoire = ctx.get("memoire_contextuelle", "").strip()

        ctx.setdefault("plugins_log", [])
        divergences = []

        # Test 1 : raisonnement vs analyse
        if raisonnement and analyse and not self._coherent(raisonnement, analyse):
            divergences.append("↯ Raisonnement vs Analyse : divergence détectée.")

        # Test 2 : raisonnement vs mémoire
        if raisonnement and memoire and not self._coherent(raisonnement, memoire):
            divergences.append("↯ Raisonnement vs Mémoire contextuelle : incohérence possible.")

        # Test 3 : analyse vs réflexion
        if analyse and reflexion and not self._coherent(analyse, reflexion):
            divergences.append("↯ Analyse vs Réflexion interne : conflit logique détecté.")

        # Action
        if divergences:
            message = "\n".join(divergences)
            ctx["reflexion_interne"] = (ctx.get("reflexion_interne", "") + "\n\n" + message).strip()
            ctx["plugins_log"].append("PluginValidationCroisée : incohérences détectées et annotées")
            logger.warning(f"[validation_croisée] Divergences :\n{message}")
        else:
            ctx["plugins_log"].append("PluginValidationCroisée : aucune incohérence détectée")

        return ctx

    def _coherent(self, texte1: str, texte2: str) -> bool:
        texte1, texte2 = texte1.lower(), texte2.lower()
        # Simple détection d'incompatibilité par négation directe
        if "non" in texte1 and "oui" in texte2:
            return False
        if any(mot in texte1 and mot not in texte2 for mot in ["erreur", "vide", "aucun"]):
            return False
        return True
