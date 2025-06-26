import logging
from noyau_core import BasePlugin, Context, Meta
import httpx

logger = logging.getLogger("plugin.planificateur_proactif")

LLM_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3"

class PluginPlanificateurProactif(BasePlugin):
    meta = Meta(
        name="plugin_planificateur_proactif",
        version="1.0",
        priority=1.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("message", "")
        intention = ctx.get("intention", "")
        objectif = ctx.get("objectif", {}).get("but", "")

        if not message.strip():
            ctx.setdefault("plugins_log", []).append("plugin_planificateur_proactif : message vide")
            return ctx

        prompt = (
            "Tu es un agent de planification intelligent. Sur la base du message utilisateur suivant, "
            "de l’intention générale et de l’objectif, produis un plan d’action sous forme de liste ordonnée, "
            "avec des étapes claires, concises, utiles à l’IA pour progresser logiquement :\n\n"
            f"Message : {message}\nIntention : {intention}\nObjectif : {objectif}\n\n"
            "Plan d’action :"
        )

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(LLM_URL, json={
                    "model": LLM_MODEL,
                    "prompt": prompt,
                    "stream": False
                })
                res.raise_for_status()
                data = res.json()
                plan_brut = data.get("response", "").strip()
        except Exception as e:
            logger.warning(f"[planificateur_proactif] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append("plugin_planificateur_proactif : erreur API")
            return ctx

        if plan_brut:
            étapes = [{"étape": step.strip(), "status": "à faire"} for step in plan_brut.split("\n") if step.strip()]
            ctx["plan_proactif"] = étapes
            ctx.setdefault("plugins_log", []).append("plugin_planificateur_proactif : plan généré")
            logger.info(f"[planificateur_proactif] Plan : {étapes}")
        return ctx
