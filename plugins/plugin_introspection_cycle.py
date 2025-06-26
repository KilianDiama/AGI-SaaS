from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.introspection_cycle")

class PluginIntrospectionCycle(BasePlugin):
    meta = Meta(
        name="plugin_introspection_cycle",
        version="1.1",  # ← version sécurisée
        priority=998,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # Sécurité : vérif type avant .strip()
        llm_response = ctx.get("llm_response", "")
        if not isinstance(llm_response, str):
            llm_response = str(llm_response)
        response = llm_response.strip()

        objectif_raw = ctx.get("objectif", {})
        if isinstance(objectif_raw, dict):
            objective = str(objectif_raw.get("but", "inconnu"))
        else:
            objective = str(objectif_raw) if objectif_raw else "inconnu"

        step = ctx.get("tache_courante", "non spécifiée")
        eval_data = ctx.get("evaluation_reponse", {})

        if not isinstance(eval_data, dict):
            eval_data = {}

        note = eval_data.get("note", 0)
        try:
            note = float(note)
        except Exception:
            note = 0.0

        feedback = eval_data.get("verdict", "aucune")

        introspection = {
            "objectif": objective,
            "étape": step,
            "note": note,
            "verdict": feedback,
            "recommandation": self.get_recommendation(note)
        }

        ctx["introspection_cycle"] = introspection
        ctx.setdefault("plugins_log", []).append("IntrospectionCycle : évaluation injectée.")
        return ctx

    def get_recommendation(self, note: float) -> str:
        if note >= 4:
            return "👍 Poursuivre le plan tel quel."
        elif note >= 2:
            return "⚠️ Vérifier la clarté de l’objectif ou relancer avec un style plus direct."
        else:
            return "🔄 Réévaluer l’intention, relancer avec un nouveau prompt ou redéfinir l’objectif."
