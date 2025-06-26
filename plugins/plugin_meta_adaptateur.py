# plugins/plugin_meta_adaptateur.py

from noyau_core import BasePlugin, Context, Meta
from statistics import mean

class PluginMetaAdaptateur(BasePlugin):
    meta = Meta(
        name="plugin_meta_adaptateur",
        version="1.0",
        priority=2.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("evolution_long_terme", [])
        if len(historique) < 3:
            ctx.setdefault("plugins_log", []).append("PluginMetaAdaptateur : pas assez de données.")
            return ctx

        notes = [snap.get("note", 0) for snap in historique[-5:] if snap.get("note") is not None]
        ajustements = sum((snap.get("ajustements", []) for snap in historique[-5:]), [])
        erreurs = sum((snap.get("erreurs", []) for snap in historique[-5:]), [])

        note_moyenne = mean(notes) if notes else 0
        ctx.setdefault("plugins_log", []).append(f"PluginMetaAdaptateur : note moyenne sur 5 = {note_moyenne:.2f}")

        meta_actions = []

        if note_moyenne < 2:
            meta_actions.append("🔁 Augmenter la température")
            ctx["llm_config"]["temperature"] = min(ctx["llm_config"].get("temperature", 0.7) + 0.2, 1.2)

        if len(erreurs) > 5:
            meta_actions.append("🛠️ Activer mode critique automatique")
            ctx["mode_critique_auto"] = True

        if "forcer clarté" in ajustements:
            meta_actions.append("🧽 Simplifier davantage le style")

        ctx["meta_actions"] = meta_actions
        ctx.setdefault("plugins_log", []).append(f"PluginMetaAdaptateur : actions suggérées = {meta_actions}")

        return ctx
