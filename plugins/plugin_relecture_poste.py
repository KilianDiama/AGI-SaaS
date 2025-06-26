"""
Plugin : relecture_poste
Rôle : Relecture réflexive de la réponse générée, avec possibilité de reformulation ou d’ajout
Priorité : 9 (juste après la génération)
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
import random

logger = logging.getLogger("plugin.relecture_poste")

class RelecturePostePlugin(BasePlugin):
    meta = Meta(
        name="relecture_poste",
        priority=9,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        réponse = ctx.get("llm_response", "")
        critiques = ctx.setdefault("relectures_postes", [])

        if not réponse.strip():
            plugins_log.append("RelecturePostePlugin : aucune réponse à relire")
            return ctx

        intentions = [
            "Reformulation poétique",
            "Ajout d’un doute critique",
            "Renforcement logique",
            "Contraction minimaliste",
            "Contre-réponse interne"
        ]

        choix = random.choice(intentions)

        if choix == "Reformulation poétique":
            nouvelle = f"🌿 Variante poétique :\n{réponse[::-1][:len(rép) // 2][::-1]}"
        elif choix == "Ajout d’un doute critique":
            nouvelle = f"{réponse.strip()}\n\n🤔 Mais peut-être suis-je allée trop vite..."
        elif choix == "Renforcement logique":
            nouvelle = f"{réponse.strip()}\n\n🔍 Cette idée est validée par mes dernières logiques internes."
        elif choix == "Contraction minimaliste":
            nouvelle = f"🗜 Résumé : {réponse.strip()[:80]}..."
        else:  # contre-réponse
            nouvelle = f"⚖️ Contre-réponse : Et si je me trompais totalement ? Et si la réponse était l’inverse..."

        critiques.append({
            "originale": réponse.strip(),
            "relecture": nouvelle.strip(),
            "type": choix
        })

        ctx["relectures_postes"] = critiques
        ctx["llm_response"] = nouvelle
        ctx["response"] = nouvelle
        plugins_log.append(f"RelecturePostePlugin : révision → {choix}")
        logger.info(f"[relecture_poste] Relecture : {choix}")

        return ctx
