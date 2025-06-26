"""
Plugin : autogen_code
Rôle : Générer dynamiquement du code Python pour sa propre évolution (auto-amélioration)
Priorité : 3.1 (juste après projection_evolution)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.autogen_code")

class AutoGenCodePlugin(BasePlugin):
    meta = Meta(
        name="autogen_code",
        priority=3.1,
        version="1.0",
        author="AGI & Matthieu"
    )

    PROMPT_TEMPLATE = (
        "Tu es une AGI capable de t'améliorer. "
        "Voici une proposition de plugin à coder : '{proposition}'. "
        "Génère uniquement le code complet, prêt à être exécuté, sans explication. "
        "Structure : plugin Python basé sur la classe BasePlugin."
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        roadmap = ctx.get("evolution_projetees", {})
        propositions = roadmap.get("propositions", [])

        if not propositions:
            plugins_log.append("AutoGenCodePlugin : aucune idée à coder.")
            return ctx

        proposition = propositions[0]
        prompt = self.PROMPT_TEMPLATE.format(proposition=proposition)

        llm = ctx.get("llm_instance")
        if not llm:
            plugins_log.append("AutoGenCodePlugin : aucun LLM disponible pour générer le code.")
            return ctx

        try:
            reponse_code = await llm.acall(prompt)
            ctx["code_autogenere"] = {
                "proposition": proposition,
                "contenu": reponse_code
            }
            plugins_log.append("AutoGenCodePlugin : code généré pour la première proposition.")
            logger.info("[autogen_code] Code produit automatiquement par AGI.")
        except Exception as e:
            plugins_log.append(f"AutoGenCodePlugin : erreur LLM → {str(e)}")
            logger.error(f"[autogen_code] Erreur de génération : {e}")

        return ctx
