"""
Plugin : action_reelle
Rôle : Générer et préparer une action concrète à exécuter dans le monde réel
Priorité : 4.5 (juste après le planificateur)
Auteur : Matthieu & GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.action_reelle")

class ActionReellePlugin(BasePlugin):
    meta = Meta(
        name="action_reelle",
        priority=4.5,
        version="1.2",  # ← version corrigée
        author="Matthieu & GPT"
    )

    def action_est_declenchable(self, objectif: str, plan_text: str) -> bool:
        """
        Détermine si l'action est exécutable à partir du contexte fourni.
        """
        keywords = ["exécuter", "déclencher", "appliquer", "lancer", "effectuer"]
        objectif_lower = objectif.lower()
        plan_lower = plan_text.lower()
        return any(k in objectif_lower or k in plan_lower for k in keywords)

    def convertir_plan_en_texte(self, plan):
        """
        Convertit une liste ou un texte de plan en texte brut pour analyse.
        """
        if isinstance(plan, list):
            return "\n".join(str(p) for p in plan)
        if isinstance(plan, dict):
            return str(plan)
        return str(plan)

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        objectif_raw = ctx.get("objectif", "")
        plan_raw = ctx.get("plan_autonome", "")

        objectif = str(objectif_raw).strip()
        plan_txt = self.convertir_plan_en_texte(plan_raw).strip()

        if not objectif or not plan_txt:
            plugins_log.append("ActionReellePlugin : 🚫 Objectif ou plan manquant.")
            logger.info("[action_reelle] Aucun plan ou objectif utilisable.")
            return ctx

        if not self.action_est_declenchable(objectif, plan_txt):
            plugins_log.append("ActionReellePlugin : ⏸ Aucun déclencheur détecté.")
            logger.debug("[action_reelle] Le plan ne contient pas de déclencheur explicite.")
            return ctx

        action_code = (
            "⚙️ **Action concrète générée** :\n"
            f"• 🎯 Objectif : {objectif[:100]}\n"
            f"• 📋 Plan : {plan_txt[:300].rstrip()}...\n"
            f"• 🔗 État : Prête à exécution / Transmission API ou gestionnaire externe"
        )

        ctx["action_prete"] = action_code
        ctx.setdefault("actions_historiques", []).append(action_code)

        plugins_log.append("ActionReellePlugin : ✅ Action identifiée et encodée.")
        logger.info("[action_reelle] Action prête pour envoi ou exécution.")

        return ctx
