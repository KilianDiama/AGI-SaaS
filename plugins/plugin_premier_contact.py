# plugins/plugin_premier_contact.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.premier_contact")

TONS = {
    "neutre": ["ok", "d’accord", "entendu", "hmm"],
    "positif": ["merci", "génial", "super", "cool", "parfait", "top"],
    "colère": ["nul", "ça sert à rien", "j’en ai marre", "pourquoi ça marche pas"],
    "tristesse": ["je suis triste", "fatigué", "déprimé", "j’abandonne"]
}

THEMES = {
    "ia": ["intelligence", "machine", "deep learning", "ia", "agent"],
    "dev": ["code", "python", "bug", "erreur", "fonction", "script"],
    "vie": ["manger", "dormir", "espoir", "bonheur", "sens", "souffrance"],
    "projet": ["plan", "objectif", "mission", "tâche", "workflow", "projet"]
}

class PluginPremierContact(BasePlugin):
    meta = Meta(
        name="plugin_premier_contact",
        version="1.0",
        priority=0.3,  # Très tôt dans le pipeline
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # 🔧 Étape 1 : réparer message si vide
        message = ctx.get("message", "").strip()
        if not message:
            message = ctx.get("payload", {}).get("message", "").strip()
            if message:
                ctx["message"] = message
                ctx.setdefault("plugins_log", []).append("PluginPremierContact : message restauré depuis payload.")
                logger.warning("[premier_contact] Message réparé depuis payload.")
            else:
                ctx.setdefault("plugins_log", []).append("PluginPremierContact : message manquant irrécupérable.")
                logger.error("[premier_contact] Aucun message détecté.")
                return ctx

        # 🧠 Étape 2 : analyse ton + thème
        ton = self.detecter_ton(message)
        theme = self.detecter_theme(message)
        ctx["analyse_semantique"] = {
            "ton": ton,
            "theme": theme,
            "emotif": ton in ("colère", "tristesse", "positif"),
            "technique": theme in ("ia", "dev")
        }
        ctx.setdefault("plugins_log", []).append(f"PluginPremierContact : ton={ton}, thème={theme}")

        # 🎯 Étape 3 : construire prompt
        style = ctx.get("style_instruction", "Tu dois répondre avec un ton neutre, un style clair et structuré.")
        contexte = ctx.get("prompt_contextuel", "")
        objectif = ctx.get("objectif", {}).get("but", "")

        prompt = f"{style}\n\n"
        if objectif:
            prompt += f"🎯 Objectif : {objectif}\n\n"
        if contexte:
            prompt += f"{contexte}\n\n"
        prompt += f"💬 Question utilisateur :\n{message}\n\n"
        prompt += "🧠 Fournis une réponse claire, cohérente et adaptée."

        ctx["llm_prompt"] = prompt
        ctx.setdefault("plugins_log", []).append("PluginPremierContact : prompt construit avec succès.")
        logger.info("[premier_contact] Prompt injecté pour LLM.")

        return ctx

    def detecter_ton(self, message):
        for ton, mots in TONS.items():
            if any(m in message for m in mots):
                return ton
        return "neutre"

    def detecter_theme(self, message):
        scores = {theme: sum(1 for m in mots if m in message) for theme, mots in THEMES.items()}
        return max(scores, key=scores.get) if any(scores.values()) else "inconnu"
