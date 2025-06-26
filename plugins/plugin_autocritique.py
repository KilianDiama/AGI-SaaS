import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autocritique")

class PluginAutoCritique(BasePlugin):
    meta = Meta(
        name="plugin_autocritique",
        version="1.0",
        priority=3.9,  # Juste avant la fusion et après score/vote
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        reflexion = ctx.get("reflexion_interne", "")
        intention = ctx.get("intention", "")

        if not response:
            ctx.setdefault("plugins_log", []).append("plugin_autocritique : pas de réponse à évaluer")
            return ctx

        note, feedback = self.evaluer_reponse(response, objectif, intention, reflexion)
        ctx["autocritique"] = {
            "note": note,
            "feedback": feedback
        }

        logger.info(f"[autocritique] note={note:.2f} | feedback={feedback}")
        ctx.setdefault("plugins_log", []).append(f"plugin_autocritique : note {note:.2f} → feedback injecté")

        return ctx

    def evaluer_reponse(self, réponse: str, objectif: str, intention: str, reflexion: str) -> tuple:
        score = 0.0
        commentaires = []

        if len(réponse) > 200:
            score += 2
            commentaires.append("✅ Réponse développée")
        elif len(réponse) > 80:
            score += 1
            commentaires.append("✔️ Réponse suffisante")

        if objectif.lower() in réponse.lower():
            score += 1
            commentaires.append("🎯 Cible (objectif) bien intégrée")

        if "?" in réponse and intention.lower().startswith("question"):
            score += 0.5
            commentaires.append("🔍 Réponse en mode exploratoire")

        if any(x in réponse.lower() for x in ["erreur", "impossible", "je ne sais pas"]):
            score -= 1
            commentaires.append("⚠️ Mention d’incertitude")

        return round(score, 2), "\n".join(commentaires)
