# plugins/plugin_prediction_style_utilisateur.py

from noyau_core import BasePlugin, Context, Meta

class PluginPredictionStyleUtilisateur(BasePlugin):
    meta = Meta(
        name="plugin_prediction_style_utilisateur",
        version="1.0",
        priority=70.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message_utilisateur", "").lower()
        tonalité = ctx.get("tonalite_utilisateur", "neutre")

        if "explique" in message or "détaille" in message:
            style = "structuré, formel"
        elif "fais court" in message or "résume" in message:
            style = "simple, concis"
        elif "inspire" in message or "idée" in message:
            style = "créatif, engageant"
        elif "besoin d'aide" in message or "conseil" in message:
            style = "empathique, rassurant"
        elif tonalité == "familier":
            style = "détendu, conversationnel"
        else:
            style = "standard, neutre"

        ctx["style_predit_utilisateur"] = style
        ctx["plugins_log"].append(f"{self.meta.name} : style prédit → {style}")
        return ctx
