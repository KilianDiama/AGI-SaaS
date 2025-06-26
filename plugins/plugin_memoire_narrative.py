# plugins/plugin_memoire_narrative.py

import os
import json
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

MEMORY_FILE = "./data/memoire_narrative.json"

class PluginMemoireNarrative(BasePlugin):
    meta = Meta(
        name="plugin_memoire_narrative",
        version="1.0",
        priority=2.5,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        current_introspection = ctx.get("introspection_critique", None)
        if not current_introspection:
            return ctx  # Rien à sauvegarder

        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, "r") as f:
                    past_data = json.load(f)
            else:
                past_data = []

            past_data.append(current_introspection)

            with open(MEMORY_FILE, "w") as f:
                json.dump(past_data[-100:], f, indent=2)  # garde les 100 derniers cycles max

            ctx.setdefault("plugins_log", []).append("PluginMemoireNarrative : introspection enregistrée.")
        except Exception as e:
            ctx.setdefault("plugins_log", []).append(f"PluginMemoireNarrative : erreur d'enregistrement ({e})")

        return ctx
