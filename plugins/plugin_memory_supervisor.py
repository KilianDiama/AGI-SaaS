# plugins/plugin_memory_supervisor.py

"""
Plugin : plugin_memory_supervisor
Rôle : Supervision de la mémoire active : taille, surcharge, injection de résumé
Priorité : 2.2 (après MemoireActivePlugin, avant tout raisonnement)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.memory_supervisor")

class PluginMemorySupervisor(BasePlugin):
    meta = Meta(
        name="plugin_memory_supervisor",
        priority=2.2,
        version="1.0",
        author="Toi & GPT"
    )

    def compter_mots(self, texte: str) -> int:
        return len(texte.split())

    async def run(self, ctx: Context) -> Context:
        historique = ctx.get("historique", [])
        total_mots = sum(self.compter_mots(m.get("message", "")) for m in historique if m.get("from") == "user")
        seuil = ctx.get("user_config", {}).get("memoire_seuil_mots", 800)

        résumé_forcé = False
        if total_mots > seuil:
            ctx["memoire_resume_force"] = True
            résumé_forcé = True
            logger.warning("[memory_supervisor] Forçage résumé mémoire : seuil dépassé.")

        ctx["memory_supervision"] = {
            "words_total": total_mots,
            "resume_forcé": résumé_forcé
        }

        ctx.setdefault("plugins_log", []).append(
            f"PluginMemorySupervisor : mots={total_mots}, résumé_forcé={résumé_forcé}"
        )

        return ctx
