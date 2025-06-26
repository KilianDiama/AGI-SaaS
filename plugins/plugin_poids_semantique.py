from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.poids_semantique")

class PluginPoidsSemantique(BasePlugin):
    meta = Meta(
        name="plugin_poids_semantique",
        version="1.0",
        priority=4.2,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("llm_response", "")
        if not texte:
            ctx.setdefault("plugins_log", []).append("plugin_poids_semantique : réponse vide")
            return ctx

        score, keywords = self.evaluer_texte(texte)
        ctx["poids_semantique"] = {
            "score": score,
            "mots_cles": keywords
        }

        logger.info(f"[plugin_poids_semantique] Score sémantique = {score:.2f} | Mots clés : {keywords}")
        ctx.setdefault("plugins_log", []).append(f"plugin_poids_semantique : score={score:.2f}")
        return ctx

    def evaluer_texte(self, texte: str) -> tuple:
        texte = texte.lower()
        mots = re.findall(r"\b\w+\b", texte)

        mots_vides = {"le", "la", "les", "de", "du", "des", "un", "une", "et", "en", "à", "au", "aux", "que", "qui", "quoi", "dont", "où"}
        significatifs = [m for m in mots if m not in mots_vides and len(m) > 3]

        frequence = {}
        for mot in significatifs:
            frequence[mot] = frequence.get(mot, 0) + 1

        poids_total = sum(frequence.values())
        score = poids_total / max(len(mots), 1)

        top_keywords = sorted(frequence.items(), key=lambda x: x[1], reverse=True)[:5]
        mots_cles = [mot for mot, freq in top_keywords]
        return score, mots_cles
