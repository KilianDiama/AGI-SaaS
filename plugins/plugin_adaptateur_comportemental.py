# plugins/plugin_adaptateur_comportemental.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.adaptateur_comportemental")

class PluginAdaptateurComportemental(BasePlugin):
    meta = Meta(
        name="plugin_adaptateur_comportemental",
        version="1.0",
        priority=98.4,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        simulations = ctx.get("simulation_futur", {}).get("scenarios", [])
        tonalite = ctx.get("tonalite_utilisateur", "neutre")
        profil = ctx.get("profil_utilisateur", {})
        style = "neutre"

        # 🔎 Analyse simple des impacts simulés
        impact_negatif = any(s.get("impact") == "négatif" and s.get("probabilite", 0) > 0.3 for s in simulations)
        impact_positif = any(s.get("impact") == "positif" and s.get("probabilite", 0) > 0.4 for s in simulations)

        # 📊 Ajustement de style comportemental
        if impact_negatif:
            style = "diplomatique et rassurant"
        elif impact_positif:
            style = "engagé et affirmatif"
        elif tonalite == "frustré":
            style = "calmant et empathique"

        ctx["style_comportemental"] = style
        ctx.setdefault("plugins_log", []).append(f"PluginAdaptateurComportemental : style ajusté → {style}")
        return ctx
