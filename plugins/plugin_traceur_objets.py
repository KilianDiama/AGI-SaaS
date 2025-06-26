from noyau_core import BasePlugin, Context, Meta
import logging
import re

logger = logging.getLogger("plugin.traceur_objets")

class PluginTraceurObjets(BasePlugin):
    meta = Meta(
        name="plugin_traceur_objets",
        version="1.0",
        priority=3.7,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        texte = ctx.get("message", "")
        objets = ctx.get("objets_suivis", set())

        nouveaux = self.extraire_objets(texte)
        objets.update(nouveaux)

        ctx["objets_suivis"] = sorted(objets)
        ctx.setdefault("plugins_log", []).append(
            f"PluginTraceurObjets : objets suivis = {ctx['objets_suivis']}"
        )

        logger.info(f"[traceur_objets] Suivi objets : {ctx['objets_suivis']}")
        return ctx

    def extraire_objets(self, texte: str) -> set:
        # Méthode naïve mais efficace pour début
        tokens = re.findall(r"\b[a-zA-Zéèêàâùïëç0-9_-]{3,}\b", texte)
        communs = {"bonjour", "merci", "plugin", "fichier", "salut", "texte", "question", "réponse"}
        objets = set(t for t in tokens if t.lower() not in communs)
        return objets
