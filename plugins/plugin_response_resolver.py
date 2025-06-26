# plugins/plugin_response_resolver.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.resolver")

class PluginResponseResolver(BasePlugin):
    meta = Meta(
        name="plugin_response_resolver",
        priority=999,  # Priorité très basse : à exécuter en dernier
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Essayons plusieurs sources possibles
        logique = ctx.get("response_logique", "").strip()
        vote = ctx.get("llm_response_votée", "").strip()
        brute = ctx.get("llm_response", "").strip()
        consolidées = ctx.get("llm_responses", [])

        # Choix prioritaire
        if logique:
            final = logique
            source = "response_logique"
        elif vote:
            final = vote
            source = "llm_response_votée"
        elif brute:
            final = brute
            source = "llm_response"
        elif consolidées:
            for r in consolidées:
                if isinstance(r, str) and r.strip():
                    final = r.strip()
                    source = "llm_responses"
                    break
            else:
                final = ""
                source = "vide"
        else:
            final = ""
            source = "vide"

        # Si rien n'a été trouvé
        if not final:
            final = "Désolé, je n'ai pas pu générer de réponse utile."
            source = "fallback"

        # Injecte dans le contexte pour le rendu final
        ctx["llm_response"] = final
        ctx["output_message"] = f"[Réponse finale] : {final}"
        ctx.setdefault("plugins_log", []).append(f"PluginResponseResolver : réponse utilisée → {source}.")
        logger.info(f"[resolver] Réponse finale = {source} ({len(final)} chars)")

        return ctx
