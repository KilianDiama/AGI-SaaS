# plugins/plugin_logique_absurdite.py

import re
import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.logique_absurdite")

class PluginLogiqueAbsurdite(BasePlugin):
    meta = Meta(
        name="plugin_logique_absurdite",
        priority=2.4,
        version="1.0",
        author="Toi & GPT"
    )

    contradictions = [
        ("je suis un humain", "je suis une IA"),
        ("toujours", "jamais"),
        ("c’est vrai", "c’est faux")
    ]

    absurde_patterns = [
        r"la terre est plate",
        r"j'ai deux cerveaux humains",
        r"le temps est carré",
        r"je vis sur mars avec des dauphins qui parlent"
    ]

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("response", "")
        if not message or not message.strip():
            ctx["absurdite_evaluee"] = {
                "coherence": False,
                "absurdite_detectee": False,
                "commentaire": "Réponse vide ou uniquement du remplissage."
            }
            ctx.setdefault("plugins_log", []).append("PluginLogiqueAbsurdite : message vide ❌")
            return ctx

        evaluation = self._evaluer(message)
        ctx["absurdite_evaluee"] = evaluation
        ctx.setdefault("plugins_log", []).append(f"PluginLogiqueAbsurdite : {evaluation['commentaire']}")
        logger.info(f"[absurdite] Analyse → {evaluation}")
        return ctx

    def _evaluer(self, message: str) -> dict:
        message = message.lower()
        for c1, c2 in self.contradictions:
            if c1 in message and c2 in message:
                return {
                    "coherence": False,
                    "absurdite_detectee": True,
                    "commentaire": f"Contradiction détectée entre '{c1}' et '{c2}'."
                }

        for pattern in self.absurde_patterns:
            if re.search(pattern, message):
                return {
                    "coherence": False,
                    "absurdite_detectee": True,
                    "commentaire": f"Contenu absurde détecté : « {pattern} »."
                }

        return {
            "coherence": True,
            "absurdite_detectee": False,
            "commentaire": "✅ Aucune absurdité ni contradiction détectée."
        }
