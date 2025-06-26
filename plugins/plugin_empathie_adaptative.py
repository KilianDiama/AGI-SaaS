# plugins/plugin_empathie_adaptative.py

"""
Plugin : plugin_empathie_adaptative
Rôle : Adapter le ton, la douceur ou l'énergie de réponse selon l’analyse sémantique
Priorité : 2.0 (après l’analyse, avant raisonneur et rédaction)
Auteur : Toi & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.empathie_adaptative")

TONS_PRESETS = {
    "colère": {
        "style_instruction": "Réponds calmement, avec empathie et assurance.",
        "réaction": "Tu sembles frustré(e), je vais t’aider pas à pas 💡."
    },
    "tristesse": {
        "style_instruction": "Sois doux, rassurant, bienveillant.",
        "réaction": "Je suis là. On va traverser ça ensemble 🌱."
    },
    "positif": {
        "style_instruction": "Réponds avec énergie et entrain.",
        "réaction": "Trop bien ! On va faire des merveilles 🤩."
    },
    "neutre": {
        "style_instruction": "Reste neutre, structuré, fluide.",
        "réaction": ""
    }
}

class PluginEmpathieAdaptative(BasePlugin):
    meta = Meta(
        name="plugin_empathie_adaptative",
        priority=2.0,
        version="1.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        sem = ctx.get("analyse_semantique", {})
        ton = sem.get("ton", "neutre")

        if ton not in TONS_PRESETS:
            ton = "neutre"

        instructions = TONS_PRESETS[ton]["style_instruction"]
        intro = TONS_PRESETS[ton]["réaction"]

        ctx["style_instruction"] = instructions
        ctx["empathie_intro"] = intro

        ctx.setdefault("plugins_log", []).append(f"plugin_empathie_adaptative : style adapté au ton « {ton} »")
        logger.info(f"[empathie] Ton : {ton} → Style : {instructions}")

        return ctx
