from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger("plugin.memoire_profonde")

class PluginMemoireProfonde(BasePlugin):
    meta = Meta(
        name="plugin_memoire_profonde",
        version="1.0",
        priority=0.9,
        author="Toi & GPT"
    )

    def _hash_text(self, text: str) -> str:
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def _resumer(self, text: str) -> str:
        # Résumé simplifié — peut être remplacé par un LLM plus tard
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return lines[0][:250] + ("..." if len(lines[0]) > 250 else "")

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        long_memoire = ctx.setdefault("memoire_profonde", {})

        for entry in historique:
            if entry.get("from") != "user":
                continue

            texte = entry.get("message", "").strip()
            if not texte:
                continue

            cle = self._hash_text(texte)
            if cle not in long_memoire:
                resume = self._resumer(texte)
                long_memoire[cle] = {
                    "résumé": resume,
                    "timestamp": datetime.utcnow().isoformat(),
                    "importance": 1.0  # Échelle future
                }
                logger.info(f"[memoire_profonde] Ajouté : {resume}")

        ctx["memoire_profonde"] = long_memoire
        ctx.setdefault("plugins_log", []).append(f"PluginMemoireProfonde : mémoire condensée avec {len(long_memoire)} entrée(s).")

        return ctx
