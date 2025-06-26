# plugin_loader.py

"""
Charge dynamiquement tous les plugins du dossier /plugins
Trie selon la priorité (meta.priority)
"""

import os
import importlib.util
from pathlib import Path

def charger_plugins():
    plugins = []

    dossier_plugins = Path(__file__).parent / "plugins"

    for fichier in os.listdir(dossier_plugins):
        if fichier.endswith(".py") and not fichier.startswith("__"):
            chemin = dossier_plugins / fichier
            spec = importlib.util.spec_from_file_location(fichier[:-3], chemin)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for nom in dir(module):
                obj = getattr(module, nom)
                if hasattr(obj, "meta") and hasattr(obj, "run"):
                    plugins.append(obj())

    # Trie par priorité décroissante
    plugins = sorted(plugins, key=lambda p: getattr(p.meta, "priority", 0))

    return plugins
