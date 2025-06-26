# plugins/llm_ollama_py.py
import logging
import ollama
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_ollama_py")

class LLMLocalOllamaPyPlugin(BasePlugin):
    meta = Meta(
        name="llm_local_ollama",
        version="1.0",
        priority=-951,   # juste après CLI si tu préfères l’API Python d’abord
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = (ctx.get("llm_prompt") or ctx.get("demande_llm", "")).strip()
        if not prompt:
            ctx["llm_response"] = ""
            ctx.setdefault("plugins_log", []).append("LLMLocalOllamaPyPlugin : prompt vide")
            return ctx

        model = ctx.get("llm_model")
        backend = ctx.get("llm_backend")
        if not model or not backend:
            logger.error("[llm_local_ollama] Modèle ou backend manquant dans le contexte.")
            ctx["llm_response"] = ""
            ctx.setdefault("plugins_log", []).append("LLMLocalOllamaPyPlugin : modèle ou backend manquant.")
            return ctx

        try:
            client = ollama.OllamaClient()
            resp = client.completion.create(
                model=model,
                prompt=prompt,
                backend=backend,
                temperature=0.7,
                max_tokens=512
            )
            text = resp.completion.strip()
        except Exception as e:
            text = ""
            logger.error(f"[llm_local_ollama] Erreur API Ollama: {e}")
            ctx.setdefault("plugins_log", []).append(f"LLMLocalOllamaPyPlugin : erreur Ollama → {e}")

        ctx["llm_response"] = text
        ctx.setdefault("plugins_log", []).append(f"LLMLocalOllamaPyPlugin : API {backend}/{model}")
        return ctx
