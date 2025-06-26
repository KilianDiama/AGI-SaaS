from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.contradiction_checker")

class PluginContradictionChecker(BasePlugin):
    meta = Meta(
        name="plugin_contradiction_checker",
        version="1.0",
        priority=4.2,  # Après vote, juste avant réponse finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("llm_response_votée", "").strip()
        if not response:
            ctx.setdefault("plugins_log", []).append("plugin_contradiction_checker : réponse vide")
            return ctx

        issues = []

        # Détection de contradiction possible
        contradiction_patterns = [
            r"\b(par contre|cependant|mais)\b.*?\b(par ailleurs|en même temps)\b",
            r"\b(c'est vrai)\b.*?\b(c'est faux|ce n'est pas vrai)\b",
        ]
        for pattern in contradiction_patterns:
            if re.search(pattern, response, flags=re.IGNORECASE | re.DOTALL):
                issues.append("🔍 Contradiction potentielle détectée")

        # Vérification d’ambiguïtés ou d’expressions floues
        expressions_floues = [
            "peut-être", "il semble que", "on pourrait penser", "il est possible que",
            "certainement", "probablement", "selon certains", "on dit que"
        ]
        flous = [exp for exp in expressions_floues if exp in response.lower()]
        if flous:
            issues.append(f"🌀 Ambiguïté détectée : {', '.join(flous)}")

        # Injection de feedback
        if issues:
            ctx["verificateur_contradiction"] = "\n".join(issues)
            ctx.setdefault("plugins_log", []).append("plugin_contradiction_checker : incohérence(s) détectée(s)")
            logger.warning(f"[contradiction_checker] Incohérences :\n{issues}")
        else:
            ctx.setdefault("plugins_log", []).append("plugin_contradiction_checker : aucun problème détecté")

        return ctx
