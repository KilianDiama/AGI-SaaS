"""
Plugin : router_decisionnel
Rôle : Déléguer les cas de doute ou d’ambiguïté à l’AGI fille spécialisée
Priorité : 4.2 (après détection d’échec ou d’incertitude)
Auteur : AGI & Matthieu
"""

import logging
import subprocess
import os
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.router_decisionnel")

class RouterDecisionnelPlugin(BasePlugin):
    meta = Meta(
        name="router_decisionnel",
        priority=4.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    def cas_flou_detecte(self, ctx: Context) -> bool:
        if "fallback" in "".join(ctx.get("plugins_log", [])).lower():
            return True
        if ctx.get("llm_response", "") == "":
            return True
        if ctx.get("eval_plugin_propose", {}).get("note", 0) < 1.0:
            return True
        return False

    def lancer_agi_fille(self, chemin_dossier: str, message: str) -> str:
        main_path = os.path.join(chemin_dossier, "main.py")
        if not os.path.exists(main_path):
            return "AGI fille non trouvée."

        try:
            result = subprocess.check_output(["python3", main_path, message], stderr=subprocess.STDOUT, text=True)
            return result.strip()
        except subprocess.CalledProcessError as e:
            return f"Erreur AGI fille : {e.output.strip()}"

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])

        if not self.cas_flou_detecte(ctx):
            plugins_log.append("RouterDecisionnelPlugin : pas de cas flou détecté.")
            return ctx

        chemin_fille = ctx.get("agi_fille_path")
        if not chemin_fille:
            plugins_log.append("RouterDecisionnelPlugin : aucune AGI fille disponible.")
            return ctx

        message = ctx.get("message", "Analyse de décision floue requise")
        resultat_fille = self.lancer_agi_fille(chemin_fille, message)

        ctx["llm_response"] = resultat_fille
        plugins_log.append("RouterDecisionnelPlugin : réponse routée depuis AGI fille.")
        logger.info("[router_decisionnel] Décision floue transférée à la fille.")

        return ctx
