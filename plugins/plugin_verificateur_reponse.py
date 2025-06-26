# plugins/plugin_verificateur_reponse.py

"""
Plugin : plugin_verificateur_reponse
Rôle : Vérifier si la réponse est complète, logique, bien structurée
Priorité : 4.1 (après génération, avant stylisation/fusion)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.verificateur_reponse")

class PluginVerificateurReponse(BasePlugin):
    meta = Meta(
        name="plugin_verificateur_reponse",
        priority=4.1,
        version="1.1",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        réponse = ctx.get("llm_response") or ctx.get("response", "")
        if not réponse.strip():
            ctx["evaluation_reponse"] = {
                "verdict": "vide",
                "note": 0,
                "longueur": 0
            }
            ctx.setdefault("plugins_log", []).append("plugin_verificateur_reponse : réponse vide.")
            return ctx

        score, verdict = self.evaluer(réponse)
        ctx["evaluation_reponse"] = {
            "verdict": verdict,
            "note": score,
            "longueur": len(réponse.strip())
        }
        ctx.setdefault("plugins_log", []).append(f"plugin_verificateur_reponse : score={score:.2f}, verdict={verdict}")
        return ctx

    def evaluer(self, texte: str) -> tuple:
        score = 0
        texte = texte.strip()
        longueur = len(texte)

        if longueur > 100:
            score += 1
        if texte.count(".") >= 2:
            score += 1
        if "?" not in texte and any(x in texte.lower() for x in ["voici", "donc", "cela signifie"]):
            score += 1
        if any(x in texte.lower() for x in ["erreur", "impossible", "invalide"]):
            score -= 2

        verdict = "acceptable" if score >= 2 else "faible"
        return max(score, 0), verdict
