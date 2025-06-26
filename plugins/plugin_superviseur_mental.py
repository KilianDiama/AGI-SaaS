# plugins/plugin_superviseur_mental.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.superviseur_mental")

class PluginSuperviseurMental(BasePlugin):
    meta = Meta(
        name="plugin_superviseur_mental",
        version="1.0",
        priority=98.5,  # après la boucle réflexive
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").lower()
        intention = ctx.get("intention", "").lower()
        reponse = ctx.get("response", "").strip()
        reflexion = ctx.get("reflexion_interne", "").lower()

        incoherences = []

        if not reponse:
            incoherences.append("Réponse vide malgré objectif actif.")
        if objectif and "aucun" in objectif and reponse:
            incoherences.append("Réponse générée sans objectif explicite.")
        if intention not in objectif:
            incoherences.append(f"Intention '{intention}' mal alignée avec objectif '{objectif}'.")

        if incoherences:
            ctx.setdefault("plugins_log", []).append("SuperviseurMental : incohérences détectées.")
            ctx["coherence_alertes"] = incoherences
            ctx["response"] += "\n\n⚠️ Alerte de supervision : incohérences détectées.\n- " + "\n- ".join(incoherences)
        else:
            ctx.setdefault("plugins_log", []).append("SuperviseurMental : cohérence OK.")

        return ctx
