# plugins/llm_openrouter.py

import httpx
import os
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_openrouter")

class OpenRouterLLMPlugin(BasePlugin):
    meta = Meta(
        name="llm_openrouter",
        priority=100,
        version="1.5",  # version corrigée
        author="Toi"
    )

    async def run(self, ctx: Context) -> Context:
        logger.info("✅ Plugin llm_openrouter activé")

        model = ctx.get("llm_model", "openai/gpt-4")
        message_user = ctx.get("message_augmenté") or ctx.get("message")

        if not isinstance(message_user, str):
            messages_list = ctx.get("messages", [])
            if isinstance(messages_list, list):
                message_user = next(
                    (m.get("content") for m in reversed(messages_list)
                     if isinstance(m, dict) and m.get("role") == "user" and isinstance(m.get("content"), str)),
                    None
                )

        if not message_user:
            logger.warning("⚠️ Aucun message utilisateur détecté dans ctx.")
            ctx["response"] = "❗ Aucun message à envoyer au modèle."
            ctx.setdefault("plugins_log", []).append("OpenRouterLLMPlugin : aucun message à traiter")
            return ctx

        messages = [{"role": "user", "content": message_user}]
        logger.debug(f"🧠 Message injecté dans OpenRouter : {message_user[:200]}")

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            error_msg = "❌ OPENROUTER_API_KEY manquant dans l'environnement."
            logger.error(error_msg)
            ctx.setdefault("errors", []).append({
                "plugin": "llm_openrouter",
                "error": error_msg
            })
            ctx["response"] = "Erreur : clé API absente."
            return ctx

        headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }

        body = {
            "model": model,
            "messages": messages
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=body
                )
                response.raise_for_status()
                data = response.json()
                reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

                if reply:
                    ctx["response"] = reply
                    logger.info(f"✅ Réponse LLM : {reply[:60]}…")
                else:
                    ctx["response"] = "❌ Réponse vide du modèle."
                    logger.warning("⚠️ Réponse vide depuis OpenRouter.")

        except Exception as e:
            logger.exception("🚨 Erreur lors de l'appel à OpenRouter")
            ctx.setdefault("errors", []).append({
                "plugin": "llm_openrouter",
                "error": str(e)
            })
            ctx["response"] = "❌ Erreur lors de l'appel OpenRouter."

        ctx.setdefault("plugins_log", []).append("OpenRouterLLMPlugin exécuté")
        return ctx
