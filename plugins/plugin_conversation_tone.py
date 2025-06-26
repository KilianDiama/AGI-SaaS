import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.conversation_tone")

class PluginConversationTone(BasePlugin):
    meta = Meta(
        name="plugin_conversation_tone",
        version="1.0",
        priority=9.5,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("response", "")
        user_config = ctx.get("user_config", {})
        tone = user_config.get("tone", "neutre")  # défaut
        style = user_config.get("style", "clair")

        if not response:
            return ctx

        # Transformations simples (peuvent être enrichies par LLM ou règles avancées)
        if tone == "empathique":
            response = f"🌷 Tu n'es pas seul·e. Voici une réponse que j'espère douce et utile :\n\n{response}"

        elif tone == "pro":
            response = f"✔️ Réponse structurée :\n\n{response}"

        elif tone == "créatif":
            response = f"🎨 Voici une réponse aux couleurs de l'imagination :\n\n{response}"

        elif tone == "enfant":
            response = f"👶 Coucou toi ! Voilà une réponse toute simple :\n\n{response}"

        # Exemples de style
        if style == "synthétique" and len(response) > 300:
            response = response[:300] + "… ✂️ (réponse abrégée)"

        ctx["response"] = response
        ctx.setdefault("plugins_log", []).append(f"PluginConversationTone : ton = {tone}, style = {style}")
        logger.info(f"[conversation_tone] Appliqué ton={tone}, style={style}")
        return ctx
