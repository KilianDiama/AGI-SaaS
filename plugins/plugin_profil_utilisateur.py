from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.profil_utilisateur")

class PluginProfilUtilisateur(BasePlugin):
    meta = Meta(
        name="plugin_profil_utilisateur",
        version="1.0",
        priority=1.4,  # Avant réflexion et raisonnement
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("history", [])
        intention = ctx.get("intention", "")
        plan = ctx.get("plan", [])
        style = ctx.get("style_instruction", "")
        message = ctx.get("message", "")

        profil = {
            "niveau_engagement": self._eval_engagement(historique),
            "ton_utilisateur": self._detect_ton(message),
            "type_intentions": list({step.get("étape", "") for step in plan}),
            "style_preferé": style.strip() if style else "standard",
        }

        ctx["profil_utilisateur"] = profil
        ctx.setdefault("plugins_log", []).append(f"PluginProfilUtilisateur : profil injecté")
        logger.info(f"[profil_utilisateur] → {profil}")
        return ctx

    def _eval_engagement(self, history):
        if not history:
            return "faible"
        if len(history) >= 10:
            return "très élevé"
        if len(history) >= 5:
            return "modéré"
        return "léger"

    def _detect_ton(self, text):
        if not text:
            return "neutre"
        text = text.lower()
        if "♥" in text or ":)" in text:
            return "chaleureux"
        if "?" in text and "!" in text:
            return "curieux"
        if "merci" in text:
            return "respectueux"
        return "neutre"
