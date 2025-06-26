# plugins/plugin_performance_guardian.py

"""
Plugin : plugin_performance_guardian
Rôle : Ajuster dynamiquement les paramètres pour éviter surcharge ou lenteur
Priorité : 2.4
Auteur : Matt & GPT
"""

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.performance_guardian")

class PluginPerformanceGuardian(BasePlugin):
    meta = Meta(
        name="plugin_performance_guardian",
        version="1.0",
        priority=2.4,
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        message = ctx.get("payload", {}).get("message", "")
        original_models = ctx.get("payload", {}).get("models", [])
        plugins_log = ctx.setdefault("plugins_log", [])

        # 1. Vérifie la taille du message
        word_count = len(message.split())
        if word_count > 500:
            plugins_log.append("plugin_performance_guardian : message long détecté → activation résumé auto")
            ctx["forcer_auto_summary"] = True

        # 2. Limite les modèles si la liste est trop longue
        if len(original_models) > 3:
            ctx["payload"]["models"] = original_models[:3]
            plugins_log.append(f"plugin_performance_guardian : réduction des modèles → {ctx['payload']['models']}")

        # 3. Prépare un tag de stratégie (optionnel)
        ctx["performance_mode"] = "guarded"
        logger.info("[plugin_performance_guardian] Mode performance activé.")
        plugins_log.append("plugin_performance_guardian : mode performance → ON")

        return ctx
