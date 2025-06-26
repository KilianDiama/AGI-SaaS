from noyau_core import BasePlugin, Context, Meta
import logging
import httpx

logger = logging.getLogger("plugin.auto_rewriter")

# Optionnellement : point d'entrée d'un backend LLM local ou distant
REWRITER_BACKEND = "http://localhost:11434/api/generate"
REWRITER_MODEL = "llama3"

class PluginAutoRewriter(BasePlugin):
    meta = Meta(
        name="plugin_auto_rewriter",
        version="1.0",
        priority=4.3,  # Juste après contradiction_checker
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        feedback = ctx.get("verificateur_contradiction", "")
        response = ctx.get("llm_response_votée", "")
        if not feedback or not response:
            ctx.setdefault("plugins_log", []).append("plugin_auto_rewriter : aucune incohérence détectée")
            return ctx

        prompt = (
            "Réécris ce texte pour corriger toute contradiction, ambiguïté ou incohérence détectée. "
            "Garde le sens original. Clarifie là où c’est flou :\n\n"
            f"---\n{response}\n---\n\n"
            f"# Feedback détecté :\n{feedback}\n\n"
            "Réponse corrigée :"
        )

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(REWRITER_BACKEND, json={
                    "model": REWRITER_MODEL,
                    "prompt": prompt,
                    "stream": False
                })
                res.raise_for_status()
                data = res.json()
                rewritten = data.get("response", "").strip()
                ctx["llm_response_votée"] = rewritten
                ctx.setdefault("plugins_log", []).append("plugin_auto_rewriter : réponse reformulée")
                logger.info("[auto_rewriter] Réécriture effectuée.")
        except Exception as e:
            logger.error(f"[auto_rewriter] Erreur lors de la reformulation : {str(e)}")
            ctx.setdefault("plugins_log", []).append(f"plugin_auto_rewriter : erreur → {str(e)}")

        return ctx
