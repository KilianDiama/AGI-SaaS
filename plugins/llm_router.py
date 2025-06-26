# plugins/llm_router.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_router")

class LLMRouterPlugin(BasePlugin):
    meta = Meta(
        name="llm_router",
        version="3.0",
        priority=5,
        author="Matt & GPT"
    )

    DEFAULT_MODEL = "llama3"
    DEFAULT_BACKEND = "ollama"

    async def run(self, ctx: Context) -> Context:
        # Récupère modèle/backend depuis le top-level payload ou utilise les valeurs par défaut
        payload = ctx.get("payload", {})
        model = payload.get("llm_model") or ctx.get("llm_models", [self.DEFAULT_MODEL])[0]
        backend = payload.get("llm_backend") or ctx.get("llm_backend", self.DEFAULT_BACKEND)

        ctx["llm_model"] = model
        ctx["llm_backend"] = backend
        # prépare la demande brute pour le plugin LLM
        ctx["demande_llm"] = ctx.get("message", "")

        logger.info(f"[llm_router] Routage LLM forcé → {backend}/{model}")
        ctx.setdefault("plugins_log", []).append(
            f"LLMRouterPlugin : routage forcé vers {backend}/{model}"
        )
        return ctx
