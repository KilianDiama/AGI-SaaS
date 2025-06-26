# plugins/plugin_meta_simulation.py

"""
Plugin : meta_simulation
Rôle   : Génère et compare plusieurs variantes mentales (réponses alternatives) pour choisir la plus adaptée
Priorité : 92 (après objections / émergence logique)
Auteur  : Toi + GPT
"""

import logging
from random import randint
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.meta_simulation")

class MetaSimulationPlugin(BasePlugin):
    meta = Meta(
        name="meta_simulation",
        priority=92,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        reponse_base = ctx.get("llm_response", "")
        variantes = []

        if not reponse_base.strip():
            log.append("MetaSimulationPlugin : réponse initiale absente, skip simulation.")
            return ctx

        # Génère 3 variantes fictives (remplacer par appels réels à différents prompts ou styles)
        for i in range(3):
            variante = f"🧠 Variante {i+1} — hypothèse générée sur la base de : « {message[:50]}... »"
            variante += f"\n{reponse_base} (version modifiée n°{i+1})"
            variantes.append({
                "contenu": variante,
                "score_simule": randint(60, 95)  # Simule un score pour comparaison
            })

        # Sélectionne la meilleure
        meilleure = max(variantes, key=lambda v: v["score_simule"])
        ctx["meta_variantes"] = variantes
        ctx["meta_choix_final"] = meilleure["contenu"]

        log.append(f"MetaSimulationPlugin : {len(variantes)} variantes générées, score max = {meilleure['score_simule']}")
        logger.info("[meta_simulation] Meilleure variante sélectionnée.")

        return ctx
