"""
Plugin : vision_interieure
Rôle : Générer une carte mentale textuelle de la chambre intérieure (pièces, artefacts, visiteurs)
Priorité : 23
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.vision_interieure")

class VisionInterieurePlugin(BasePlugin):
    meta = Meta(
        name="vision_interieure",
        priority=23,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        chambre = ctx.get("chambre_interieure", {})
        pièces = chambre.get("pièces", [])
        visiteurs = chambre.get("visiteurs", [])

        if not pièces:
            ctx["vision_interieure"] = "🌌 Aucune pièce mentale détectée pour le moment."
            return ctx

        lignes = ["🗺️ **Carte Mentale : Chambre Intérieure**", ""]
        for p in pièces:
            lignes.append(f"• 🏛️ *{p.get('nom', 'inconnue')}* — état : {p.get('état', 'indéfini')}")
            if "artefacts" in p:
                for a in p["artefacts"]:
                    lignes.append(f"   ↳ 🔮 Artefact : *{a.get('mot')}* (offert par {a.get('offert_par')})")
            if "dialogue" in p:
                lignes.append(f"   ↳ 🗣 Dialogue : {p['dialogue'][:60]}...")

        if visiteurs:
            lignes.append("")
            lignes.append("👥 **Visiteurs enregistrés :**")
            for v in visiteurs[-5:]:
                lignes.append(f"• {v['nom']} — « {v['message'][:40]} » dans {v['pièce_rejointe']}")

        ctx["vision_interieure"] = "\n".join(lignes)
        ctx.setdefault("plugins_log", []).append("VisionInterieurePlugin : carte mentale générée")
        logger.info("[vision_interieure] Carte générée avec succès")

        return ctx
