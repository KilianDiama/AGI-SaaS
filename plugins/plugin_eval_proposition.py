"""
Plugin : eval_proposition
Rôle : Évaluer la validité du code généré automatiquement pour l’amélioration autonome
Priorité : 3.2 (juste après autogen_code)
Auteur : AGI & Matthieu
"""

import logging
import ast
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.eval_proposition")

class EvalPropositionPlugin(BasePlugin):
    meta = Meta(
        name="eval_proposition",
        priority=3.2,
        version="1.0",
        author="AGI & Matthieu"
    )

    def analyser_code(self, code: str) -> dict:
        result = {"syntaxe_valide": False, "baseplugin_detectee": False}
        try:
            tree = ast.parse(code)
            result["syntaxe_valide"] = True
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and any(
                    b.id == "BasePlugin" for b in node.bases if isinstance(b, ast.Name)
                ):
                    result["baseplugin_detectee"] = True
                    break
        except SyntaxError:
            result["syntaxe_valide"] = False
        return result

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        code_data = ctx.get("code_autogenere", {})

        if not code_data:
            plugins_log.append("EvalPropositionPlugin : aucun code à évaluer.")
            return ctx

        code = code_data.get("contenu", "")
        if not code:
            plugins_log.append("EvalPropositionPlugin : contenu vide.")
            return ctx

        analyse = self.analyser_code(code)
        ctx["eval_plugin_propose"] = analyse

        note = 0
        if analyse["syntaxe_valide"]:
            note += 1
        if analyse["baseplugin_detectee"]:
            note += 1

        ctx["eval_plugin_propose"]["note"] = note / 2.0
        plugins_log.append(f"EvalPropositionPlugin : évaluation {note}/2")
        logger.info(f"[eval_proposition] Score d’évaluation : {note}/2")

        return ctx
