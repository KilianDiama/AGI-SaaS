# plugins/plugin_style_adapter.py

"""
Plugin : plugin_style_adapter
Rôle : Adapter la réponse à un style donné (neutre, pro, humoristique, etc.)
Priorité : 4.2 (après vérif structure, avant export ou affichage)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.style_adapter")

class PluginStyleAdapter(BasePlugin):
    meta = Meta(
        name="plugin_style_adapter",
        priority=4.2,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("llm_response") or ctx.get("response", "")
        if not texte.strip():
            ctx.setdefault("plugins_log", []).append("plugin_style_adapter : pas de texte à styliser")
            return ctx

        style = ctx.get("style_instruction", "neutre clair structuré").lower()
        logger.info(f"[style_adapter] Style demandé : {style}")

        adapted = self.adapte_style(texte, style)
        ctx["response"] = adapted
        ctx.setdefault("plugins_log", []).append(f"plugin_style_adapter : style '{style}' appliqué")

        return ctx

    def adapte_style(self, texte: str, style: str) -> str:
        # Exemple simple d’adaptation (peut être remplacé par LLM plus tard)
        if "humour" in style:
            return f"{texte.strip()} 😄 (PS : c’est une réponse pleine d’esprit !)"
        elif "pro" in style:
            return f"[Réponse professionnelle]\n\n{texte.strip()}"
        elif "empathique" in style:
            return f"💬 *Je comprends...*\n\n{texte.strip()}"
        elif "poétique" in style:
            return f"🌸 *Voici une réponse toute en douceur :*\n\n{texte.strip()}"
        else:
            # Style neutre/clair/structuré
            return texte.strip()

