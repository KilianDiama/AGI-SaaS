# plugins/plugin_user_config_loader.py

import json
import os
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.user_config_loader")

class UserConfigLoaderPlugin(BasePlugin):
    meta = Meta(
        name="plugin_user_config_loader",
        version="1.0",
        priority=-900,  # Avant les vérifs d'accès ou LLM
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        user_id = ctx.get("user_id", "anonymous")
        config_path = "data/users.json"

        if not os.path.isfile(config_path):
            logger.warning("[UserConfigLoader] Fichier users.json introuvable.")
            ctx["user_config"] = self.default_config(user_id)
            return ctx

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                users_data = json.load(f)
            user_config = users_data.get(user_id, self.default_config(user_id))
            ctx["user_config"] = user_config
            ctx.setdefault("plugins_log", []).append("UserConfigLoader : config utilisateur chargée")
        except Exception as e:
            logger.error(f"[UserConfigLoader] Erreur chargement config : {e}")
            ctx["user_config"] = self.default_config(user_id)

        return ctx

    def default_config(self, user_id: str) -> dict:
        return {
            "user_id": user_id,
            "allowed_models": ["mistral", "llama3"],
            "external_keys": {
                "openai": None
            },
            "quota": {
                "max_calls_per_day": 100,
                "calls_today": 0
            }
        }
