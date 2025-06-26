import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.coherence_convers")

class PluginCoherenceConvers(BasePlugin):
    meta = Meta(
        name="plugin_coherence_convers",
        version="1.0",
        priority=1.3,  # Avant planificateur et raisonneur
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        history = ctx.get("history", [])
        response = ctx.get("llm_response", "")
        if not history or not response:
            ctx.setdefault("plugins_log", []).append("plugin_coherence_convers : pas d'historique ou de réponse")
            return ctx

        last_user_message = None
        for turn in reversed(history):
            if turn["from"] == "user":
                last_user_message = turn["message"]
                break

        if not last_user_message:
            ctx.setdefault("plugins_log", []).append("plugin_coherence_convers : aucun message utilisateur trouvé")
            return ctx

        if self._is_off_topic(response, last_user_message):
            correction = (
                "[⚠️ Incohérence détectée] : la réponse semble déconnectée du dernier message utilisateur.\n"
                "Il est recommandé de reformuler ou de réinterpréter le contexte."
            )
            ctx["coherence_warning"] = correction
            ctx.setdefault("plugins_log", []).append("plugin_coherence_convers : incohérence détectée")
            logger.warning(f"[coherence_convers] → {correction}")
        else:
            ctx.setdefault("plugins_log", []).append("plugin_coherence_convers : OK")

        return ctx

    def _is_off_topic(self, response: str, message: str) -> bool:
        """Heuristique simple de cohérence thématique"""
        keywords_msg = set(message.lower().split())
        keywords_resp = set(response.lower().split())
        intersection = keywords_msg & keywords_resp
        return len(intersection) < 3  # seuil ajustable
