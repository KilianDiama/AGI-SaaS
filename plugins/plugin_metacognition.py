from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.metacognition")

class PluginMetacognition(BasePlugin):
    meta = Meta(
        name="plugin_metacognition",
        priority=4.8,  # Juste avant la réponse finale
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        response = ctx.get("response", "")
        note = ctx.get("evaluation_reponse", {}).get("note", 0)
        objectif = ctx.get("objectif", {}).get("but", "inconnu")
        intention = ctx.get("intention", "non définie")

        reflexion = []

        # Analyse qualité de la réponse
        if note < 2:
            reflexion.append("⚠️ La réponse générée semble peu satisfaisante.")
        elif note >= 4:
            reflexion.append("✅ Réponse jugée pertinente et complète.")

        # Auto-évaluation des étapes de pensée
        if "raisonneur" not in ctx.get("composition_dynamique", []):
            reflexion.append("❓ Raisonneur non activé : vérifier si utile pour cet objectif.")
        if not ctx.get("llm_response"):
            reflexion.append("⛔ Aucune réponse directe du LLM n’a été fournie.")
        if ctx.get("reflexion_interne"):
            reflexion.append("🧠 Une réflexion interne a bien été réalisée.")

        # Synthèse
        message = f"🧩 **Auto-évaluation du cycle**\n" \
                  f"- Intention : {intention}\n" \
                  f"- Objectif : {objectif}\n" \
                  f"- Note de réponse : {note}/5\n\n" \
                  f"Commentaires :\n" + "\n".join(reflexion)

        ctx["meta_reflexion"] = message
        log.append("PluginMetacognition : réflexion métacognitive injectée.")
        logger.info("[metacognition] Auto-évaluation réalisée.")

        return ctx
