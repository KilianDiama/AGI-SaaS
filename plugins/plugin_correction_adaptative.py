from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.correction_adaptative")

class PluginCorrectionAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_correction_adaptative",
        version="1.0",
        priority=4.3,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse_initiale = ctx.get("llm_response", "")
        simulations = ctx.get("simulations_futures", {}).get("scenarios", [])

        if not reponse_initiale or not simulations:
            logger.info("[plugin_correction_adaptative] Pas de réponse ou de simulations → plugin ignoré.")
            return ctx

        # Analyse des scénarios négatifs
        risque_detecte = any(s["impact"] == "négatif" and s["probabilite"] > 0.2 for s in simulations)

        if not risque_detecte:
            logger.info("[plugin_correction_adaptative] Aucun risque significatif détecté.")
            ctx.setdefault("plugins_log", []).append("plugin_correction_adaptative : pas de correction nécessaire.")
            return ctx

        # Correction simple : ajout d’un disclaimer ou reformulation douce
        reponse_corrigee = self.adapte_reponse(reponse_initiale)
        ctx["llm_response"] = reponse_corrigee
        ctx.setdefault("plugins_log", []).append("plugin_correction_adaptative : réponse ajustée pour prévenir les risques.")
        logger.info("[plugin_correction_adaptative] Réponse modifiée en prévention d’un scénario à risque.")
        return ctx

    def adapte_reponse(self, texte: str) -> str:
        correction = (
            "\n\n🛡️ *Note : Cette réponse est générée automatiquement. "
            "Si elle ne vous convient pas totalement, n’hésitez pas à demander une reformulation.*"
        )
        if correction in texte:
            return texte  # Évite doublons
        return texte.strip() + correction
