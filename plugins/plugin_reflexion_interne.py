from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.reflexion_interne")

class PluginReflexionInterne(BasePlugin):
    meta = Meta(
        name="plugin_reflexion_interne",
        priority=1.4,
        version="1.2",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        raw_message = ctx.get("message", "")
        if isinstance(raw_message, dict):
            raw_message = raw_message.get("content", "")
        message = raw_message.strip()

        if not message or len(message) < 3:
            ctx.setdefault("plugins_log", []).append("PluginReflexionInterne : message trop court pour analyse.")
            logger.warning("[reflexion_interne] Message insuffisant pour une réflexion utile.")
            return ctx

        reflexion = []

        # 1. Intention implicite
        if "?" in message:
            reflexion.append("💡 Message interrogatif — intention probable : obtenir une réponse ou un conseil.")
        elif any(kw in message.lower() for kw in ["comment", "pourquoi", "faut", "faire", "devenir"]):
            reflexion.append("💬 Intention implicite détectée — formulation d’un besoin ou d’un objectif.")
        else:
            reflexion.append("📌 Message non interrogatif — possible constat, opinion ou remarque.")

        # 2. Clarté et complexité
        if len(message) < 10:
            reflexion.append("⚠️ Message très court — risque d’ambiguïté élevé.")
        elif len(message) > 500:
            reflexion.append("📚 Message long — segmentation recommandée pour éviter l’ambiguïté.")

        # 3. Structure implicite attendue
        if any(k in message.lower() for k in ["liste", "étapes", "points", "éléments"]):
            reflexion.append("🧩 Structure attendue : réponse en liste.")
        if any(k in message.lower() for k in ["expliquer", "détaille", "raconte", "développe"]):
            reflexion.append("🧠 Demande explicative ou descriptive probable.")
        if "plan" in message.lower():
            reflexion.append("🗺️ Attente probable : plan d'action structuré.")

        # Résultat
        commentaire = "\n".join(reflexion)
        ctx["reflexion_interne"] = commentaire
        ctx.setdefault("plugins_log", []).append("PluginReflexionInterne : réflexion générée.")
        logger.info(f"[reflexion_interne] Réflexion générée :\n{commentaire}")

        return ctx
