# plugins/plugin_introspection_critique.py

from noyau_core import BasePlugin, Context, Meta
import datetime

class PluginIntrospectionCritique(BasePlugin):
    meta = Meta(
        name="plugin_introspection_critique",
        version="1.0",
        priority=4.6,  # Juste après la conscience narrative
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        erreurs = ctx.get("coherence_alertes", "")
        feedback = ctx.get("meta_critique", "")
        trace = ctx.get("trace_comportement", [])
        critique = []

        if erreurs:
            critique.append(f"⚠️ Erreurs ou incohérences détectées : {erreurs}")
        if "alignement faible" in feedback:
            critique.append("❗ Problème d’alignement détecté. Mieux analyser l’intention utilisateur.")
        if any("vide" in t.get("contenu", "").lower() for t in trace):
            critique.append("🔄 Réponse vide détectée. Ajouter un fallback LLM ou régénération.")

        if not critique:
            critique = ["✅ Aucun problème majeur détecté ce cycle."]

        introspection = {
            "timestamp": datetime.datetime.now().isoformat(),
            "analyse": critique
        }

        ctx["introspection_critique"] = introspection
        ctx.setdefault("plugins_log", []).append("PluginIntrospectionCritique : introspection critique injectée.")
        return ctx
