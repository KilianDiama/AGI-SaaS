# plugins/plugin_adaptation_comportementale.py

from noyau_core import BasePlugin, Context, Meta

class PluginAdaptationComportementale(BasePlugin):
    meta = Meta(
        name="plugin_adaptation_comportementale",
        version="1.0",
        priority=2.7,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        tendances = ctx.get("tendance_adaptative")
        if not tendances or "top_erreurs" not in tendances:
            ctx.setdefault("plugins_log", []).append("PluginAdaptationComportementale : aucune tendance disponible.")
            return ctx

        ajustements = []

        for erreur, _ in tendances["top_erreurs"]:
            if "réponse vide" in erreur or "réponse floue" in erreur:
                ajustements.append("forcer clarté")
                ctx["style"] = "très clair, phrases courtes"
            elif "incohérence intention" in erreur:
                ajustements.append("activer plugin_coherence_intentionnelle")
                ctx["forcé_plugins"] = ctx.get("forcé_plugins", []) + ["plugin_coherence_intentionnelle"]
            elif "structure absente" in erreur:
                ajustements.append("ajouter plugin_planificateur")

        if ajustements:
            ctx["ajustements_comportementaux"] = ajustements
            ctx.setdefault("plugins_log", []).append(f"PluginAdaptationComportementale : ajustements = {ajustements}")
        else:
            ctx.setdefault("plugins_log", []).append("PluginAdaptationComportementale : rien à ajuster.")

        return ctx
