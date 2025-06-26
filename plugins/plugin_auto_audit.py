from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.auto_audit")

class PluginAutoAudit(BasePlugin):
    meta = Meta(
        name="plugin_auto_audit",
        version="1.0",
        priority=3.2,  # Juste après le raisonneur, avant la fusion ou sélection
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response") or ctx.get("llm_response_votée", "")
        if not response:
            ctx.setdefault("plugins_log", []).append("plugin_auto_audit : aucune réponse à auditer")
            return ctx

        feedback = self.evaluer_reponse(response)

        ctx["audit_critique"] = feedback
        ctx.setdefault("plugins_log", []).append("plugin_auto_audit : audit critique injecté")
        logger.info(f"[auto_audit] Feedback critique :\n{feedback}")

        return ctx

    def evaluer_reponse(self, texte: str) -> str:
        lignes = []

        if len(texte.strip()) < 30:
            lignes.append("⚠️ La réponse semble trop courte pour être utile.")

        if texte.count("?") > 3:
            lignes.append("🔍 Trop de questions dans la réponse — manque d'affirmation.")

        if "je ne sais pas" in texte.lower() or "désolé" in texte.lower():
            lignes.append("🤔 La réponse évite le sujet — considérer reformulation.")

        if "**" not in texte and "-" not in texte and "\n" not in texte:
            lignes.append("📄 Absence de structure ou mise en forme — peut nuire à la lisibilité.")

        if not lignes:
            lignes.append("✅ Aucun problème critique détecté dans la réponse.")

        return "\n".join(lignes)
