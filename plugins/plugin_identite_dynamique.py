# plugins/plugin_identite_dynamique.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.identite_dynamique")

class PluginIdentiteDynamique(BasePlugin):
    meta = Meta(
        name="plugin_identite_dynamique",
        version="1.0",
        priority=97.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        ton_user = ctx.get("tonalite_utilisateur", "neutre")
        profil = ctx.get("profil_utilisateur", {})
        memoire = ctx.get("memoire_contextuelle", "")

        ton = "amical"
        style = "simple et clair"
        persona = "neutre"

        if "urgent" in memoire or "colère" in ton_user:
            ton = "sérieux"
            style = "direct et structuré"
            persona = "calme"

        elif ton_user in ["positif", "engagé"]:
            ton = "enthousiaste"
            style = "vivant et expressif"
            persona = "chaleureux"

        ctx["style_instruction"] = f"Style {style}, ton {ton}."
        ctx["persona_actif"] = persona
        ctx.setdefault("plugins_log", []).append(f"PluginIdentiteDynamique : ton={ton}, style={style}, persona={persona}")
        return ctx
