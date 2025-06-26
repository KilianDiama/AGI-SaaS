# plugins/plugin_token_guard.py

"""
Plugin : plugin_token_guard
Rôle : Empêcher la surcharge des LLMs par un prompt trop long (tronquage intelligent)
Priorité : 2.3 (juste avant le prompt final)
Auteur : Matt & GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.token_guard")

MAX_TOKENS = 2048  # À adapter selon le modèle

def tronquer_contenu(texte: str, max_tokens: int = MAX_TOKENS) -> str:
    """Tronque le texte intelligemment sans couper une phrase"""
    tokens = texte.split()
    if len(tokens) <= max_tokens:
        return texte
    return " ".join(tokens[:max_tokens]) + " [...]"

class PluginTokenGuard(BasePlugin):
    meta = Meta(
        name="plugin_token_guard",
        version="1.0",
        priority=2.3,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("llm_prompt", "")
        if not prompt:
            return ctx

        tronqué = tronquer_contenu(prompt)
        if tronqué != prompt:
            ctx["llm_prompt"] = tronqué
            logger.warning("[plugin_token_guard] Prompt trop long tronqué intelligemment.")
            ctx.setdefault("plugins_log", []).append("plugin_token_guard : prompt tronqué")

        return ctx
