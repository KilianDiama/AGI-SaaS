# plugins/llm_multiopenrouter.py

import httpx
import os
import logging
from typing import List
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_multiopenrouter")


class MultiOpenRouterLLMPlugin(BasePlugin):
    meta = Meta(
        name="llm_multiopenrouter",
        priority=105,
        version="1.0",
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        logger.info("✅ Plugin multi LLM OpenRouter activé")

        models: List[str] = ctx.get("llm_models", [])
        backends: List[str] = ctx.get("llm_backends", [])
        message = ctx.get("message_augmenté") or ctx.get("message")

        if not models or not backends or not message:
            logger.warning("⚠️ Données incomplètes (modèles ou message manquants)")
            ctx["response"] = "❗ Aucun message ou modèle valide fourni."
            return ctx

        # Vérification longueur cohérente
        if len(models) != len(backends):
            logger.error("❌ Les longueurs de llm_models et llm_backends ne correspondent pas.")
            ctx["response"] = "❌ Configuration incorrecte : modèles et backends doivent être appariés."
            return ctx

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            ctx["response"] = "❌ Clé API OpenRouter manquante."
            return ctx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        responses = []

        for model in models:
            body = {
                "model": model,
                "messages": [{"role": "user", "content": message}]
            }

            try:
                async with httpx.AsyncClient() as client:
                    logger.info(f"🔁 Appel OpenRouter → {model}")
                    resp = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=body,
                        timeout=30.0
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    logger.info(f"✅ Réponse reçue de {model}: {text[:100]}")
                    if text:
                        responses.append(f"🔹 *{model}* → {text}")
            except Exception as e:
                err_msg = f"❌ Erreur avec {model} → {str(e)}"
                logger.warning(err_msg)
                ctx.setdefault("errors", []).append({"plugin": "llm_multiopenrouter", "error": err_msg})

        # Fusion simple des réponses
        if responses:
            fusion = "\n\n".join(responses)
            ctx["response"] = f"🤖 **Fusion multi-LLM :**\n\n{fusion}"
        else:
            ctx["response"] = "❌ Aucune réponse obtenue des modèles."

        ctx.setdefault("plugins_log", []).append("MultiOpenRouterLLMPlugin exécuté")
        return ctx
