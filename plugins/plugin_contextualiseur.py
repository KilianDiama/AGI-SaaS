from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.contextualiseur")

class PluginContextualiseur(BasePlugin):
    meta = Meta(
        name="plugin_contextualiseur",
        version="1.0",
        priority=2.2,  # Avant génération de la réponse
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        contexte_ext = []
        historique = ctx.get("historique_conversation", [])
        memoire_long_terme = ctx.get("memoire_long_terme", "")
        objectif = ctx.get("objectif", {}).get("but", "")

        if historique:
            dernieres = historique[-3:] if len(historique) > 3 else historique
            extraits = [m["message"] for m in dernieres if m.get("from") == "user"]
            if extraits:
                contexte_ext.append("📌 Derniers échanges :\n" + "\n".join(f"- {e}" for e in extraits))

        if memoire_long_terme:
            contexte_ext.append(f"🧠 Mémoire longue :\n{memoire_long_terme.strip()}")

        if objectif:
            contexte_ext.append(f"🎯 Objectif courant : {objectif}")

        if contexte_ext:
            injection = "\n\n".join(contexte_ext)
            ctx["prompt_contextuel"] = injection
            ctx.setdefault("plugins_log", []).append("PluginContextualiseur : contexte enrichi injecté")
            logger.info("[contextualiseur] Contexte enrichi injecté dans le prompt.")
        else:
            logger.info("[contextualiseur] Aucun contexte détecté à injecter.")

        return ctx
