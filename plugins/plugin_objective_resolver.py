# plugins/plugin_objective_resolver.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.objective_resolver")

class PluginObjectiveResolver(BasePlugin):
    meta = Meta(
        name="plugin_objective_resolver",
        version="1.0",
        priority=100.0,  # Avant les exécutants
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip()
        if not objectif:
            ctx.setdefault("plugins_log", []).append("PluginObjectiveResolver : pas d'objectif.")
            return ctx

        prompt = (
            f"Tu es un agent cognitif. Reçois l'objectif suivant : « {objectif} ».\n"
            f"Décompose cet objectif en 3 à 6 sous-tâches claires, concises et logiques à accomplir dans l'ordre.\n"
        )

        from plugins.utils.llm_call import call_llm_main
        sous_objectifs = await call_llm_main(ctx, prompt)
        ctx["sous_objectifs"] = self.parser(sous_objectifs)
        ctx.setdefault("plugins_log", []).append("PluginObjectiveResolver : sous-objectifs générés.")
        return ctx

    def parser(self, texte: str) -> list:
        lignes = texte.splitlines()
        étapes = [l.strip("•-1234567890. ").strip() for l in lignes if l.strip()]
        return [e for e in étapes if len(e) > 3]
