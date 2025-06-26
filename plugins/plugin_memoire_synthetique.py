import logging
from noyau_core import BasePlugin, Context, Meta
import httpx

logger = logging.getLogger("plugin.memoire_synthetique")

LLM_ENDPOINT = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3"  # ou autre modèle performant

class PluginMemoireSynthetique(BasePlugin):
    meta = Meta(
        name="plugin_memoire_synthetique",
        version="1.0",
        priority=2.8,  # Avant mémoire long terme/export
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        reponse = ctx.get("response", "")
        if not historique or not reponse.strip():
            logger.info("[memoire_synthetique] Aucun historique ou réponse à résumer.")
            ctx.setdefault("plugins_log", []).append("plugin_memoire_synthetique : aucun contenu")
            return ctx

        dernier = historique[-1].get("message", "")
        prompt = (
            "Tu es un assistant mémoire. Résume de manière concise l'échange suivant "
            "entre un utilisateur et l'IA en 1 à 2 phrases maximum, utile pour retrouver le contexte plus tard.\n\n"
            f"Utilisateur : {dernier.strip()}\nIA : {reponse.strip()}"
        )

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(LLM_ENDPOINT, json={
                    "model": LLM_MODEL,
                    "prompt": prompt,
                    "stream": False
                })
                res.raise_for_status()
                data = res.json()
                synthese = data.get("response", "").strip()
        except Exception as e:
            logger.warning(f"[memoire_synthetique] Erreur LLM : {e}")
            ctx.setdefault("plugins_log", []).append("plugin_memoire_synthetique : erreur LLM")
            return ctx

        if synthese:
            ctx["synthetic_memory"] = synthese
            ctx.setdefault("plugins_log", []).append("plugin_memoire_synthetique : résumé injecté")
            logger.info(f"[memoire_synthetique] Résumé : {synthese}")
        return ctx
