# plugins/plugin_emotion_dynamique.py

from noyau_core import BasePlugin, Context, Meta

class PluginEmotionDynamique(BasePlugin):
    meta = Meta(
        name="plugin_emotion_dynamique",
        version="1.0",
        priority=75.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message_utilisateur", "").lower()
        tonalité = ctx.get("tonalite_utilisateur", "neutre")

        if "merci" in message or "génial" in message:
            emotion = "satisfaction"
        elif "je suis perdu" in message or "j'y arrive pas":
            emotion = "empathie"
        elif "vas-y" in message or "on continue":
            emotion = "enthousiasme"
        elif "c'est nul" in message or "ça bug":
            emotion = "frustration légère"
        else:
            emotion = "calme"

        ctx["emotion_simulee"] = emotion
        ctx["plugins_log"].append(f"{self.meta.name} : émotion simulée → {emotion}")
        return ctx
