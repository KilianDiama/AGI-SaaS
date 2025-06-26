# plugins/plugin_conscience_narrative.py

from noyau_core import BasePlugin, Context, Meta
from datetime import datetime

class PluginConscienceNarrative(BasePlugin):
    meta = Meta(
        name="plugin_conscience_narrative",
        version="1.0",
        priority=78.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("historique", [])
        emotions = []
        intentions = []
        themes = []

        for message in historique[-10:]:
            txt = message.get("message", "").lower()
            if "agi" in txt or "intelligence générale" in txt:
                themes.append("AGI")
            if "continuons" in txt:
                intentions.append("poursuivre")
            if "bug" in txt or "nul" in txt:
                emotions.append("frustration")
            if "parfait" in txt or "super" in txt:
                emotions.append("enthousiasme")

        état_narratif = {
            "theme_dominant": max(set(themes), key=themes.count) if themes else "non défini",
            "emotion_dominante": max(set(emotions), key=emotions.count) if emotions else "neutre",
            "intention_récurrente": max(set(intentions), key=intentions.count) if intentions else "indéterminée",
            "mise_a_jour": datetime.utcnow().isoformat()
        }

        ctx["conscience_narrative"] = état_narratif
        ctx["plugins_log"].append(
            f"{self.meta.name} : thème={état_narratif['theme_dominant']}, "
            f"émotion={état_narratif['emotion_dominante']}, "
            f"intention={état_narratif['intention_récurrente']}"
        )
        return ctx
