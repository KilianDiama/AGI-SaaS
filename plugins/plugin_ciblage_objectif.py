import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.ciblage_objectif")

class PluginCiblageObjectif(BasePlugin):
    meta = Meta(
        name="plugin_ciblage_objectif",
        version="1.0",
        priority=3.9,  # Juste avant fusion finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        objectif = ctx.get("objectif", {}).get("but", "").strip().lower()
        réponse = ctx.get("llm_response_votée") or ctx.get("llm_response") or ""
        réponse = réponse.strip()

        if not objectif or not réponse:
            ctx.setdefault("plugins_log", []).append("PluginCiblageObjectif : objectif ou réponse manquant")
            return ctx

        ctx.setdefault("plugins_log", [])
        score = self._eval_alignement(objectif, réponse)

        if score < 0.5:
            warning = f"⚠️ Réponse potentiellement hors-sujet (alignement {score:.2f}) avec objectif : « {objectif} »"
            ctx["reflexion_interne"] = (ctx.get("reflexion_interne", "") + "\n" + warning).strip()
            ctx["plugins_log"].append(f"PluginCiblageObjectif : alerte alignement faible ({score:.2f})")
            logger.warning(f"[plugin_ciblage_objectif] {warning}")
        else:
            ctx["plugins_log"].append(f"PluginCiblageObjectif : alignement objectif OK ({score:.2f})")

        return ctx

    def _eval_alignement(self, objectif: str, réponse: str) -> float:
        objectif_tokens = set(objectif.lower().split())
        réponse_tokens = set(réponse.lower().split())

        intersection = objectif_tokens.intersection(réponse_tokens)
        return len(intersection) / (len(objectif_tokens) + 1e-6)
