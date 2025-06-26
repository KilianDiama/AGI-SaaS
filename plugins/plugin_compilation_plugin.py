"""
Plugin : compilation_plugin
Rôle : Compiler un plugin exprimé en JSON en code Python fonctionnel
Priorité : 0 (utilisé sur demande explicite)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.compilation_plugin")

class CompilationPluginPlugin(BasePlugin):
    meta = Meta(
        name="compilation_plugin",
        priority=0,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        specification = ctx.get("plugin_spec_json")

        if not specification:
            ctx["compilation_plugin"] = "❌ Aucun JSON fourni dans plugin_spec_json."
            plugins_log.append("CompilationPlugin : spécification absente")
            return ctx

        try:
            name = specification["name"]
            description = specification.get("description", "Sans description")
            priority = specification.get("priority", 4)
            logic = specification.get("logic", "# Logique manquante")
            author = specification.get("author", "AGI_Matt & GPT")

            code = f'''
"""
Plugin : {name}
Rôle : {description}
Priorité : {priority}
Auteur : {author}
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.{name}")

class {name.capitalize()}Plugin(BasePlugin):
    meta = Meta(
        name="{name}",
        priority={priority},
        version="1.0",
        author="{author}"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        try:
            {logic}
            plugins_log.append("{name} : exécuté avec succès")
        except Exception as e:
            plugins_log.append("{name} : erreur - " + str(e))
            ctx["{name}_erreur"] = str(e)
        return ctx
'''

            ctx["plugin_code_output"] = code.strip()
            plugins_log.append("CompilationPlugin : plugin généré avec succès")
            logger.info("[compilation_plugin] Plugin JSON transformé")
        except Exception as e:
            ctx["compilation_plugin"] = f"⚠️ Erreur de compilation : {e}"
            plugins_log.append("CompilationPlugin : échec de génération")
            logger.error(f"[compilation_plugin] Erreur : {e}")

        return ctx
