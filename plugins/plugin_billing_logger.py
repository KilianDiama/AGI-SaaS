# plugins/plugin_billing_logger.py

import os
import json
import time
from noyau_core import BasePlugin, Context, Meta

LOG_PATH = "logs/billing_logs.jsonl"

class PluginBillingLogger(BasePlugin):
    meta = Meta(
        name="plugin_billing_logger",
        version="1.0",
        priority=990,  # Juste avant la réponse finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        if ctx.get("rejected"):
            return ctx  # Ne rien logguer si rejet (quota, auth, etc.)

        user_id = ctx.get("user_config", {}).get("user_id", "anonymous")
        model = ctx.get("llm_model", "unknown")
        backend = ctx.get("llm_backend", "unknown")
        prompt = ctx.get("llm_prompt", "")[:300]  # tronqué
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        log_entry = {
            "user_id": user_id,
            "timestamp": timestamp,
            "model": model,
            "backend": backend,
            "prompt_preview": prompt,
            "cycle_id": ctx.get("cycle_id", "none"),
        }

        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        ctx.setdefault("plugins_log", []).append("PluginBillingLogger : log de facturation ajouté.")
        return ctx
