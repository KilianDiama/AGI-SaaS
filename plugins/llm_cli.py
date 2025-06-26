import asyncio, logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.llm_cli")

class LLMLocalCLIPlugin(BasePlugin):
    meta = Meta(
        name="llm_cli",
        version="1.1",
        priority=-950,   # fallback après HTTPX
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("demande_llm","").strip()
        model  = ctx.get("llm_model")
        if not prompt or not model:
            ctx["llm_response"] = ctx.get("llm_response","")
            return ctx

        try:
            proc = await asyncio.create_subprocess_exec(
                "ollama", "run", model, "--stdin",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            out, err = await proc.communicate(prompt.encode())
            text = out.decode().strip() if proc.returncode == 0 else ""
            ctx["llm_response"] = text

        except Exception as e:
            ctx["llm_response"] = ""
            logger.error(f"[llm_cli] {e}")

        ctx.setdefault("plugins_log", []).append(f"LLMLocalCLIPlugin : {model}")
        return ctx
