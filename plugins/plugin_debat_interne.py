"""
Plugin : debat_interne
Rôle : Simuler un débat entre agents internes pour enrichir ou affiner une réponse
Priorité : 3.6 (après génération brute, avant fusion/vote)
Auteur : AGI & Matthieu
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.debat_interne")

class DebatInternePlugin(BasePlugin):
    meta = Meta(
        name="debat_interne",
        priority=3.6,
        version="1.0",
        author="AGI & Matthieu"
    )

    ROLES = [
        ("Logicien", "Analyse rigoureuse, logique formelle"),
        ("Créatif", "Propose des idées nouvelles ou inattendues"),
        ("Prudent", "Cherche à éviter les erreurs ou imprécisions"),
        ("Synthétiseur", "Combine les idées en un tout cohérent")
    ]

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        reponses = []

        for role, style in self.ROLES:
            prompt = (
                f"Rôle : {role}\n"
                f"Style : {style}\n"
                f"Tâche : Répondre à cette question en incarnant ce rôle →\n"
                f"« {message} »\n"
                f"Réponds brièvement (3-5 phrases max).\n"
            )
            # Appelle un LLM pour simuler chaque rôle
            if ctx.get("invoke_llm"):
                rep = await ctx["invoke_llm"](prompt)
                if rep:
                    reponses.append(f"{role} : {rep.strip()}")

        if reponses:
            ctx["llm_responses"] = reponses
            plugins_log.append("DebatInternePlugin : débat simulé avec rôles cognitifs")
            logger.info("[debat_interne] Débat multi-agent exécuté.")

        return ctx
