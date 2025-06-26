from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.synthese_contextuelle")

class PluginSyntheseContextuelle(BasePlugin):
    meta = Meta(
        name="plugin_synthese_contextuelle",
        version="1.0",
        priority=1.3,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "inconnu")
        reflexion = ctx.get("reflexion_interne", "")
        memoire = ctx.get("memoire_profonde", {})
        etape = ctx.get("tache_courante", "non spécifiée")

        resume_memoire = "\n".join(
            f"- {item['résumé']}" for item in memoire.values()
        )

        synthese = f"""🎯 Objectif : {objectif}

🧠 Réflexion :
{reflexion or "Aucune réflexion disponible."}

📌 Étape actuelle : {etape}

🗃️ Mémoires récentes :
{resume_memoire or "Aucune mémoire profonde disponible."}
"""

        ctx["synthese_contextuelle"] = synthese.strip()
        ctx.setdefault("plugins_log", []).append("PluginSyntheseContextuelle : synthèse injectée dans le contexte.")
        logger.info(f"[synthese_contextuelle] Synthèse générée ({len(synthese)} caractères)")

        return ctx
