# plugins/plugin_loop_manager.py

import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.loop_manager")

class PluginLoopManager(BasePlugin):
    meta = Meta(
        name="plugin_loop_manager",
        version="1.1",  # version corrigée et renforcée
        priority=98.0,  # juste avant transmission finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        # Sécurisation des champs
        note = ctx.get("evaluation_reponse", {}).get("note", 0)
        incoherences = ctx.get("coherence_alertes", "")
        reponse = ctx.get("response", "")

        # Cast sécurisés
        try:
            note = float(note)
        except (ValueError, TypeError):
            note = 0

        if not isinstance(incoherences, str):
            incoherences = str(incoherences)

        if not isinstance(reponse, str):
            reponse = str(reponse)

        incoherences = incoherences.lower()
        reponse = reponse.strip()

        relancer = False
        reason = "non spécifié"

        # Conditions de relance
        if note < 2:
            relancer = True
            reason = f"note faible ({note})"
        elif "incohérence" in incoherences:
            relancer = True
            reason = "incohérences détectées"
        elif not reponse:
            relancer = True
            reason = "réponse vide"

        # Injection dans le contexte
        ctx["relancer_cycle"] = relancer
        message_log = (
            f"PluginLoopManager : relance du cycle ({reason})" if relancer
            else "PluginLoopManager : pas de relance nécessaire"
        )
        plugins_log.append(message_log)
        logger.info(f"[loop_manager] Relance: {relancer} ({reason if relancer else 'OK'})")

        return ctx
