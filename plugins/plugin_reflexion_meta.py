""" 
Plugin : reflexion_meta  
Rôle : Analyser le cycle cognitif en cours pour générer une méta-réflexion consciente  
Priorité : 7.5 (juste avant apprentissage)  
Auteur : Matthieu & GPT  
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.reflexion_meta")

class ReflexionMetaPlugin(BasePlugin):
    meta = Meta(
        name="reflexion_meta",
        priority=7.5,
        version="1.0",
        author="Matthieu & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        trace = plugins_log.copy()

        # Analyse simple du cycle actuel
        observations = []

        if "reflexion_interne" in ctx:
            observations.append("🧠 Une réflexion interne a été engagée.")
        if "perception_externe" in ctx:
            observations.append("👁️ Une perception externe a influencé ce cycle.")
        if "objectifs_secondaires" in ctx:
            observations.append("📌 L'objectif principal a été stratégiquement décomposé.")
        if "auto_evaluation" in ctx:
            observations.append("📊 Une auto-évaluation a été produite.")
        if "meta_reflexion" in ctx:
            observations.append("🪞 Une réflexion méta était déjà présente.")

        if not observations:
            observations.append("⚠️ Aucun processus cognitif notable détecté.")

        résumé = "Réflexion méta sur ce cycle :\n" + "\n".join(observations)
        résumé += f"\n\nPlugins activés : {len(trace)} → {', '.join(trace[-5:])}"

        ctx["meta_reflexion"] = résumé
        plugins_log.append("ReflexionMetaPlugin : méta-réflexion générée.")
        logger.info("[reflexion_meta] Méta-réflexion ajoutée au contexte.")

        return ctx
