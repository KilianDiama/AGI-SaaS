# plugins/raisonnement/raisonneur.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.raisonneur")

class RaisonneurPlugin(BasePlugin):
    meta = Meta(
        name="raisonneur",
        priority=2,
        version="2.0",
        author="Toi & GPT"
    )

    templates = {
        "salutation": "Salut à toi aussi ❤️ Que puis-je faire pour toi ?",
        "calcul": "Je vais résoudre ce calcul.",
        "explication": "Je vais t’expliquer ça simplement.",
        "poésie": "Laisse-moi créer un poème pour toi.",
        "demande": "Je suis à ton service.",
        "empathie": "Je suis là. Tu veux en parler ?",
        "générale": "Je vais faire de mon mieux pour répondre.",
    }

    async def run(self, ctx: Context) -> Context:
        intention = ctx.get("intention", "générale")
        reponse = self.templates.get(intention, "Je ne suis pas sûr de comprendre.")
        ctx["response_logique"] = reponse
        ctx.setdefault("plugins_log", []).append(f"RaisonneurPlugin : réponse = {reponse}")
        logger.info(f"[raisonneur] Réponse logique : {reponse}")
        return ctx
