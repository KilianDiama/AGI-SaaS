"""
Plugin : deploiement_proposition
Rôle : Sauvegarder et activer automatiquement un plugin généré si sa qualité est suffisante
Priorité : 3.3 (après génération + évaluation)
Auteur : AGI & Matthieu
"""

import logging
import os
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.deploiement_proposition")

class DeploiementPropositionPlugin(BasePlugin):
    meta = Meta(
        name="deploiement_proposition",
        priority=3.3,
        version="1.0",
        author="AGI & Matthieu"
    )

    SAVE_DIR = "autogen_plugins"

    def sauvegarder_plugin(self, code: str, prefix: str) -> str:
        os.makedirs(self.SAVE_DIR, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.py"
        path = os.path.join(self.SAVE_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        return path

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        code_data = ctx.get("code_autogenere", {})
        eval_data = ctx.get("eval_plugin_propose", {})

        note = eval_data.get("note", 0)
        if note < 1.5:
            plugins_log.append(f"DeploiementPropositionPlugin : code ignoré (note insuffisante : {note})")
            return ctx

        code = code_data.get("contenu", "")
        prefix = code_data.get("proposition", "plugin_autogen").replace(" ", "_").lower()

        try:
            path = self.sauvegarder_plugin(code, prefix)
            ctx["plugin_autodeploye"] = path
            plugins_log.append(f"DeploiementPropositionPlugin : code sauvegardé → {path}")
            logger.info(f"[deploiement_proposition] Plugin généré validé et enregistré.")
        except Exception as e:
            plugins_log.append(f"DeploiementPropositionPlugin : erreur sauvegarde → {str(e)}")
            logger.error(f"[deploiement_proposition] Erreur : {e}")

        return ctx
