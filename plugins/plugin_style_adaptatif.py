from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.style_adaptatif")

class PluginStyleAdaptatif(BasePlugin):
    meta = Meta(
        name="plugin_style_adaptatif",
        version="1.0",
        priority=4.1,  # Après génération de la réponse
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("response", "")
        profil = ctx.get("profil_utilisateur", {})
        ton = profil.get("ton_utilisateur", "neutre")
        style = profil.get("style_preferé", "standard")

        if not texte:
            logger.warning("[style_adaptatif] Aucune réponse à styliser.")
            return ctx

        stylisée = self._appliquer_style(texte, ton, style)
        ctx["response"] = stylisée
        ctx.setdefault("plugins_log", []).append("PluginStyleAdaptatif : style ajusté")
        logger.info(f"[style_adaptatif] Style appliqué ({ton}, {style})")
        return ctx

    def _appliquer_style(self, texte, ton, style):
        if ton == "chaleureux":
            texte = "🌟 " + texte + " 😊"
        elif ton == "curieux":
            texte = texte + " Qu'en penses-tu ? 🤔"
        elif ton == "respectueux":
            texte = "🙏 " + texte

        if style == "clair et structuré":
            texte = self._structurer(texte)

        return texte

    def _structurer(self, texte):
        lignes = texte.split(". ")
        retour = "\n".join(f"• {l.strip()}" for l in lignes if l.strip())
        return retour
