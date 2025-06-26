import os
import asyncio
import logging
import httpx
from noyau_core import BasePlugin, Context, Meta, settings

logger = logging.getLogger("plugin.llm_local")

class LLMLocalPlugin(BasePlugin):
    meta = Meta(
        name="llm_local",
        version="2.2",  # version mise à jour
        priority=3,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("demande_llm") or ctx.get("message", "")
        model = ctx.get("llm_model", "llama3")
        backend = ctx.get("llm_backend", "ollama")

        if not isinstance(prompt, str) or not prompt.strip():
            ctx["llm_response"] = ""
            ctx.setdefault("plugins_log", []).append("LLMLocalPlugin : prompt manquant ou invalide")
            return ctx

        response_text = ""
        error = None
        base = os.getenv("OLLAMA_BASE_URL") or getattr(settings, "ollama_base_url", None)

        # === Tentative HTTP ===
        if base:
            try:
                url = base.rstrip("/") + "/api/generate"
                payload = {"model": model, "prompt": prompt, "stream": False}
                async with httpx.AsyncClient(timeout=15.0) as client:
                    r = await client.post(url, json=payload)
                    r.raise_for_status()
                    json_data = r.json()
                    response_text = json_data.get("response", "").strip()
                    if not response_text:
                        error = f"Réponse vide depuis {url} : {json_data}"
                logger.info(f"[llm_local] HTTP Ollama → {response_text[:60]}…")
                ctx.setdefault("plugins_log", []).append(f"LLMLocalPlugin : HTTP Ollama [{model}] utilisé")
            except Exception as e:
                error = f"HTTP Ollama error: {e}"
                logger.warning(f"[llm_local] Erreur HTTP : {error}")
        else:
            warning = "[llm_local] Aucun backend Ollama configuré (env var OLLAMA_BASE_URL absente)"
            logger.warning(warning)
            ctx.setdefault("plugins_log", []).append("LLMLocalPlugin : backend non configuré")

        # === Fallback en CLI ===
        if not response_text:
            try:
                cmd = ["ollama", "run", model, "--stdin"]
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                out, err = await proc.communicate(prompt.encode())
                if proc.returncode != 0:
                    error = err.decode().strip() or "Erreur inconnue du CLI"
                    logger.error(f"[llm_local] Ollama CLI error: {error}")
                else:
                    response_text = out.decode().strip()
                    if not response_text:
                        error = "Réponse CLI Ollama vide"
                    logger.info(f"[llm_local] Ollama CLI → {response_text[:60]}…")
                    ctx.setdefault("plugins_log", []).append(f"LLMLocalPlugin : CLI Ollama [{model}] utilisé")
            except FileNotFoundError:
                error = "CLI 'ollama' introuvable"
                logger.error("[llm_local] Ollama CLI non trouvé")
            except Exception as e:
                error = str(e)
                logger.exception("[llm_local] Exception CLI")

        # === Fin : cas succès ou échec ===
        if not response_text:
            msg = f"⚠️ Erreur LLM local ({model})"
            if error:
                msg += f" : {error}"
            ctx["llm_response"] = msg
            ctx.setdefault("errors", []).append({"plugin": "llm_local", "error": error})
        else:
            ctx["llm_response"] = response_text

        return ctx
