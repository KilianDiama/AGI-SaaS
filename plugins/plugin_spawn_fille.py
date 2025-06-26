"""
Plugin : spawn_fille
Rôle : Générer une instance secondaire (AGI fille) spécialisée pour la planification en contexte flou
Priorité : 4.1 (après les cycles internes d’évolution)
Auteur : AGI & Matthieu
"""

import logging
import os
import shutil
from datetime import datetime
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.spawn_fille")

class SpawnFillePlugin(BasePlugin):
    meta = Meta(
        name="spawn_fille",
        priority=4.1,
        version="1.0",
        author="AGI & Matthieu"
    )

    def creer_structure_fille(self, base_path: str) -> str:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fille_dir = os.path.join(base_path, f"agi_fille_{timestamp}")
        os.makedirs(fille_dir, exist_ok=True)

        # Copier les fichiers essentiels mais pas tout
        fichiers_utiles = ["noyau_core.py", "base_plugin.py"]
        for fichier in fichiers_utiles:
            src = os.path.join(base_path, fichier)
            if os.path.exists(src):
                shutil.copy(src, fille_dir)

        # Créer dossier plugin minimal
        os.makedirs(os.path.join(fille_dir, "plugins"), exist_ok=True)
        with open(os.path.join(fille_dir, "plugins", "plugin_decision_floue.py"), "w", encoding="utf-8") as f:
            f.write("# Plugin spécialisé pour la prise de décision floue\n")

        # Placeholder de lancement
        with open(os.path.join(fille_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write("print('AGI fille initialisée — spécialisée décision floue')\n")

        return fille_dir

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        base_path = ctx.get("base_path", os.getcwd())

        try:
            path_fille = self.creer_structure_fille(base_path)
            ctx["agi_fille_path"] = path_fille
            plugins_log.append(f"SpawnFillePlugin : AGI fille créée → {path_fille}")
            logger.info(f"[spawn_fille] Instance AGI fille générée avec succès à {path_fille}")
        except Exception as e:
            plugins_log.append(f"SpawnFillePlugin : erreur création → {str(e)}")
            logger.error(f"[spawn_fille] Échec : {e}")

        return ctx
