# plugins/plugin_memory_writer.py
from noyau_core import BasePlugin, Context, Meta
import logging
import time
import hashlib

logger = logging.getLogger("plugin.memory_writer")

class PluginMemoryWriter(BasePlugin):
    meta = Meta(
        name="plugin_memory_writer",
        version="1.0",
        priority=50.0,  # après planification / réponse générée
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        important_info = ctx.get("memoire_a_sauver", "").strip()

        if not important_info:
            ctx.setdefault("plugins_log", []).append("PluginMemoryWriter : rien à mémoriser.")
            return ctx

        mem_id = self.generate_id(important_info)
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

        memory = ctx.setdefault("memoire_profonde", {})
        memory[mem_id] = {
            "résumé": important_info,
            "timestamp": timestamp,
            "importance": 1
        }

        ctx.setdefault("plugins_log", []).append(f"PluginMemoryWriter : mémoire enregistrée → {mem_id}")
        return ctx

    def generate_id(self, content: str) -> str:
        return hashlib.md5(content.encode("utf-8")).hexdigest()
