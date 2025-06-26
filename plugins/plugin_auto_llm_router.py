# plugins/plugin_auto_llm_router.py

from noyau_core import BasePlugin, Context, Meta

class PluginAutoLLMRouter(BasePlugin):
    meta = Meta(
        name="plugin_auto_llm_router",
        version="1.0",
        priority=2.5,
        author="GPT+Toi"
    )

    async def run(self, ctx: Context) -> Context:
        payload = ctx.setdefault("payload", {})
        user = ctx.get("user_config", {})
        default_backend = "ollama"
        default_model = "mistral"

        # Si rien n’est défini, on route par défaut
        payload.setdefault("backend", user.get("preferred_backend", default_backend))
        payload.setdefault("model", user.get("preferred_model", default_model))

        # Si plusieurs modèles, on suppose backend = ollama
        if "models" in payload:
            payload["backend"] = "ollama"

        ctx.setdefault("plugins_log", []).append("plugin_auto_llm_router : backend/model définis")
        return ctx
