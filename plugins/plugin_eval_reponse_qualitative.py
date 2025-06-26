from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.eval_qualite")

class PluginEvalQualiteReponse(BasePlugin):
    meta = Meta(
        name="plugin_eval_qualite_reponse",
        version="1.0",
        priority=2.1,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        reponse = ctx.get("llm_response", "").strip()
        eval_data = {
            "longueur": len(reponse.split()),
            "vide": not bool(reponse),
            "contient_question": "?" in reponse,
            "contient_emotion": any(emo in reponse for emo in ["❤️", "😢", "😀", "👏", "🙏"]),
            "utilite_presumee": "oui" if any(k in reponse.lower() for k in ["voici", "tu peux", "exemple", "solution"]) else "non",
        }

        score = 1.0
        if eval_data["vide"]:
            score = 0.0
        elif eval_data["longueur"] > 300:
            score = 0.6
        elif eval_data["utilite_presumee"] == "oui":
            score = 0.9

        commentaire = (
            f"🧪 **Évaluation réponse IA :**\n"
            f"- 📏 Longueur : {eval_data['longueur']} mots\n"
            f"- ❔ Contient une question ? {'Oui' if eval_data['contient_question'] else 'Non'}\n"
            f"- ❤️ Émotion détectée ? {'Oui' if eval_data['contient_emotion'] else 'Non'}\n"
            f"- 🎯 Utilité présumée : {eval_data['utilite_presumee']}\n"
            f"- 🧠 Score final : {score:.2f}"
        )

        ctx["evaluation_reponse"] = {
            "score": score,
            "commentaire": commentaire
        }
        ctx.setdefault("plugins_log", []).append("PluginEvalQualiteReponse : évaluation faite.")
        logger.info(f"[eval qualité] Score : {score:.2f}\n{commentaire}")
        return ctx
