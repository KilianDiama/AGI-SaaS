# plugins/plugin_model_access_guard.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin_model_access_guard")

class ModelAccessGuardPlugin(BasePlugin):
    meta = Meta(
        name="plugin_model_access_guard",
        version="1.0",
        priority=0,  # Peut être placé avant routage LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        user_id = ctx.get("user_id", "anonymous")
        model_requested = ctx.get("payload", {}).get("data", {}).get("models", [])
        allowed_models = ctx.get("user_config", {}).get("allowed_models", [])

        # Fallback de sécurité
        if not model_requested:
            return ctx

        for model in model_requested:
            if model not in allowed_models:
                logger.warning(f"[ModelAccessGuard] {user_id} tente d'accéder à {model} sans autorisation.")
                ctx["error"] = f"Modèle {model} non autorisé pour votre compte."
                ctx["interrompre_cycle"] = True
                return ctx

        ctx.setdefault("plugins_log", []).append("ModelAccessGuard : accès aux modèles validé.")
        return ctx
