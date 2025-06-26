import logging
import httpx
from noyau_core import BasePlugin, Context, Meta, settings

logger = logging.getLogger("plugin.llm_local_httpx")

class LLMLocalHTTPXPlugin(BasePlugin):
    meta = Meta(
        name="llm_local_httpx",
        version="1.1",  # version mise à jour
        priority=10,    # après router(5), avant CLI(-950)
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt_raw = ctx.get("demande_llm", "")
        prompt = prompt_raw.strip() if isinstance(prompt_raw, str) else ""
        model = ctx.get("llm_model")
        backend = ctx.get("llm_backend")
        text = ""

        try:
            if backend == "ollama":
                base_url = getattr(settings, "ollama_base_url", None)
                if not base_url:
                    raise ValueError("OLLAMA_BASE_URL non défini")
                url = base_url.rstrip("/") + "/api/generate"
                payload = {"model": model, "prompt": prompt, "stream": False}
                async with httpx.AsyncClient(timeout=30) as client:
                    res = await client.post(url, json=payload)
                    res.raise_for_status()
                    try:
                        text = res.json().get("response", "").strip()
                    except Exception as je:
                        raise ValueError(f"Erreur parsing JSON Ollama: {je}")

            elif backend == "lmstudio":
                url = "http://localhost:1234/v1/completions"
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "temperature": 0.7,
                    "max_tokens": 512
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    res = await client.post(url, json=payload)
                    res.raise_for_status()
                    try:
                        text = res.json()["choices"][0]["text"].strip()
                    except Exception as je:
                        raise ValueError(f"Erreur parsing JSON LMStudio: {je}")

            else:
                raise ValueError(f"Backend inconnu: {backend}")

            ctx["llm_response"] = text
            ctx.setdefault("plugins_log", []).append(
                f"LLMLocalHTTPXPlugin : {backend}/{model}"
            )
            logger.info(f"[llm_local_httpx] {backend}/{model} → {text[:60]}…")

        except Exception as e:
            ctx["llm_response"] = ""
            ctx.setdefault("errors", []).append({
                "plugin": "llm_local_httpx",
                "error": str(e)
            })
            logger.error(f"[llm_local_httpx] Erreur: {e}")

        return ctx
