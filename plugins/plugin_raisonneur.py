from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.raisonneur")

class PluginRaisonneur(BasePlugin):
    meta = Meta(
        name="plugin_raisonneur",
        version="1.1",  # ← version sécurisée
        priority=2.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        history = ctx.get("history", [])
        message_utilisateur = ""
        if isinstance(history, list) and history:
            last = history[-1]
            if isinstance(last, dict):
                message_utilisateur = str(last.get("message", ""))

        objectif_raw = ctx.get("objectif", {})
        objectif = ""
        if isinstance(objectif_raw, dict):
            objectif = str(objectif_raw.get("but", ""))
        elif isinstance(objectif_raw, str):
            objectif = objectif_raw

        memoire = ctx.get("memoire_contextuelle", "")
        ref = ctx.get("reflexion_interne", "")
        plan = ctx.get("plan", [])
        tache = ctx.get("tache_courante", "")

        base_reponse = "Voici ma réponse en tenant compte de ta demande :\n\n"

        if isinstance(ref, str) and ref.strip():
            base_reponse += f"🧠 Réflexion :\n{ref.strip()}\n\n"

        if isinstance(memoire, str) and memoire.strip():
            base_reponse += f"🧾 Contexte :\n{memoire.strip()}\n\n"

        if isinstance(plan, list) and plan:
            étapes = []
            for etape in plan:
                if isinstance(etape, dict):
                    nom = etape.get("étape", "étape inconnue")
                    statut = etape.get("status", "indéfini")
                    étapes.append(f"- {nom} ({statut})")
            if étapes:
                base_reponse += "🧭 Plan :\n" + "\n".join(étapes) + "\n\n"

        base_reponse += f"📌 Étape en cours : {tache if isinstance(tache, str) else 'non définie'}\n\n"
        base_reponse += f"✉️ Message reçu : « {message_utilisateur} »\n"
        base_reponse += f"🎯 Objectif : {objectif if objectif else 'non défini'}\n\n"
        base_reponse += "🗣️ Réponse synthétique : Je vais faire de mon mieux pour répondre de façon pertinente."

        ctx["response_logique"] = base_reponse
        ctx.setdefault("plugins_log", []).append("RaisonneurPlugin : réponse synthétique générée.")
        logger.info("[raisonneur] Réponse synthétique structurée injectée.")
        return ctx
