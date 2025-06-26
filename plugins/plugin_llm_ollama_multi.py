"""
Plugin : plugin_llm_ollama_multi
Rôle : Interroger plusieurs modèles via Ollama en parallèle
Priorité : 3.5 (après routing, avant fusion)
Auteur : Matt & GPT
"""

import asyncio
import logging
from typing import List, Dict, Union

import httpx
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_ollama_multi")

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

class PluginLLMOllamaMulti(BasePlugin):
    meta = Meta(
        name="plugin_llm_ollama_multi",
        version="1.2",
        priority=3.5,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        payload = ctx.get("payload", {})
        raw_models: Union[str, List[str]] = payload.get("model", [])
        message: str = payload.get("message", "")
        backend: str = payload.get("backend", "")

        # Normalisation
        if isinstance(raw_models, str):
            models = [raw_models]
        elif isinstance(raw_models, list):
            models = raw_models
        else:
            models = []

        if backend.lower() != "ollama":
            ctx.setdefault("plugins_log", []).append("plugin_llm_ollama_multi : backend ≠ ollama, ignoré")
            return ctx

        if not models or not message:
            ctx.setdefault("plugins_log", []).append("plugin_llm_ollama_multi : modèles ou message manquants")
            return ctx

        logger.info(f"[plugin_llm_ollama_multi] Appel parallèle des modèles : {models}")
        responses: Dict[str, str] = {}

        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = [self._ask_model(client, model, message) for model in models]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        for model, result in zip(models, results):
            if isinstance(result, Exception):
                err_msg = f"Erreur : {str(result)}"
                logger.error(f"[plugin_llm_ollama_multi] {model} → {err_msg}")
                responses[model] = err_msg
            else:
                clean = result.strip()
                responses[model] = clean
                logger.info(f"[plugin_llm_ollama_multi] {model} → Réponse OK (longueur : {len(clean)} caractères)")

        ctx["llm_responses"] = [f"[{model}]\n{resp}" for model, resp in responses.items()]
        ctx.setdefault("plugins_log", []).append(
            f"plugin_llm_ollama_multi : réponses collectées {list(responses.keys())}"
        )

        return ctx

    async def _ask_model(self, client: httpx.AsyncClient, model_name: str, prompt: str) -> str:
        try:
            response = await client.post(
                OLLAMA_ENDPOINT,
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except httpx.HTTPStatusError as e:
            return f"Erreur HTTP {e.response.status_code} : {e.response.text}"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"[plugin_llm_ollama_multi] Exception dans {model_name} : {str(e)}\n{tb}")
            return f"Exception ({model_name}) : {str(e)}"
