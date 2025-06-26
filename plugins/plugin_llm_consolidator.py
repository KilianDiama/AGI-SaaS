import asyncio
import logging
import httpx
from typing import Dict
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_consolidator")

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

class PluginLLMConsolidator(BasePlugin):
    meta = Meta(
        name="plugin_llm_consolidator",
        version="1.1",  # ← mis à jour
        priority=4.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        payload = ctx.get("payload", {})
        models = payload.get("model", [])
        message = payload.get("message", "")
        backend = payload.get("backend", "").lower()

        if backend != "ollama" or not message.strip():
            ctx.setdefault("plugins_log", []).append("plugin_llm_consolidator : backend ≠ ollama ou message vide")
            return ctx

        if isinstance(models, str):
            models = [models]

        responses: Dict[str, str] = {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = [self._query_model(client, m, message) for m in models]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        for model, result in zip(models, results):
            if isinstance(result, Exception):
                responses[model] = f"[Erreur] {str(result)}"
            else:
                responses[model] = result.strip() or "[⚠️ Réponse vide]"

        # Sélection de la meilleure réponse
        valid_responses = {m: r for m, r in responses.items() if "[Erreur]" not in r and len(r) > 30}
        best_model, best_response = next(iter(valid_responses.items()), (None, ""))

        ctx["llm_responses"] = responses
        ctx["response"] = self._reformulate(best_response)
        ctx["response_summary"] = f"Réponse sélectionnée : {best_model}" if best_model else "Aucune réponse exploitable"

        log_msg = f"plugin_llm_consolidator : réponse de {best_model} utilisée." if best_model else "plugin_llm_consolidator : aucune réponse valide."
        ctx.setdefault("plugins_log", []).append(log_msg)

        return ctx

    async def _query_model(self, client: httpx.AsyncClient, model: str, prompt: str) -> str:
        try:
            resp = await client.post(OLLAMA_ENDPOINT, json={
                "model": model,
                "prompt": prompt,
                "stream": False
            })
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")
        except Exception as e:
            return f"[Erreur] {str(e)}"

    def _reformulate(self, text: str) -> str:
        if not text:
            return "🤖 Aucune réponse exploitable n'a pu être générée."
        return f"💡 Synthèse IA : {text.strip()}"
