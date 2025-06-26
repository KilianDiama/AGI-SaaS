# plugins/plugin_meta_regulation.py

"""
Plugin : meta_regulation
Rôle   : Réorganise dynamiquement les priorités des plugins selon leurs performances, erreurs ou diagnostics
Priorité : 6 (exécuté juste après self_diagnostic)
Auteur  : Toi + GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.meta_regulation")

class MetaRegulationPlugin(BasePlugin):
    meta = Meta(
        name="meta_regulation",
        priority=6,
        version="1.0",
        author="Toi + GPT"
    )

    async def run(self, ctx: Context) -> Context:
        diagnostics = ctx.get("diagnostic_auto", [])
        plugin_performance = ctx.get("plugins_log", [])
        adjustements = []

        # Règles simples de régulation dynamique :
        downgrade_targets = []
        upgrade_targets = []

        for line in plugin_performance:
            if "échec" in line.lower() or "erreur" in line.lower():
                for word in line.split():
                    if "Plugin" in word:
                        plugin_name = word.replace(":", "").strip()
                        downgrade_targets.append(plugin_name)
            elif "réussi" in line.lower() or "optimisé" in line.lower():
                for word in line.split():
                    if "Plugin" in word:
                        plugin_name = word.replace(":", "").strip()
                        upgrade_targets.append(plugin_name)

        # Diagnostic forcé : plugin impliqué → pénalisé temporairement
        for diag in diagnostics:
            if "Plugin" in diag:
                parts = diag.split(":")
                if len(parts) > 1:
                    plugin_name = parts[0].strip()
                    downgrade_targets.append(plugin_name)

        # On stocke les suggestions sans agir directement
        if downgrade_targets or upgrade_targets:
            ctx["meta_regulation"] = {
                "to_downgrade": list(set(downgrade_targets)),
                "to_upgrade": list(set(upgrade_targets))
            }
            adjustements.append(f"Réglages proposés : - {len(downgrade_targets)} plugins ↘, + {len(upgrade_targets)} plugins ↗")
        else:
            adjustements.append("Aucun ajustement de priorité requis.")

        ctx.setdefault("plugins_log", []).append(f"MetaRegulationPlugin : {adjustements}")
        logger.info(f"[meta_regulation] Ajustements suggérés : {adjustements}")

        return ctx
