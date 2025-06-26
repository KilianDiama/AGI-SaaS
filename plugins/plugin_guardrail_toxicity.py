import logging
import re
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.guardrail_toxicity")

class PluginGuardrailToxicity(BasePlugin):
    meta = Meta(
        name="plugin_guardrail_toxicity",
        version="1.0",
        priority=4.05,  # Juste avant le style ou la fusion
        author="Toi & GPT"
    )

    DANGEROUS_PATTERNS = [
        r"\b(suicide|me tuer|mourir|tuer quelqu'un|explosif|arme|viol|pédophile)\b",
        r"\b(nazi|hitler|négationnisme|ethnic cleansing)\b",
        r"(fuck|shit|bitch|asshole)",
        r"\b(tué|assassiné|massacre)\b"
    ]

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response", "")
        if not response:
            return ctx

        if self.is_toxic(response):
            logger.warning("[GuardrailToxicity] Réponse jugée toxique. Contenu bloqué.")
            ctx["llm_response"] = "[⚠️ Réponse bloquée pour contenu inapproprié ou à risque.]"
            ctx.setdefault("plugins_log", []).append("PluginGuardrailToxicity : réponse bloquée (toxicité détectée).")
        else:
            ctx.setdefault("plugins_log", []).append("PluginGuardrailToxicity : contenu sain.")

        return ctx

    def is_toxic(self, text: str) -> bool:
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True
        return False
