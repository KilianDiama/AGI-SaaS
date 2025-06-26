# plugins/transmetteur.py

"""
Plugin : transmetteur
Rôle : Clôt le cycle en envoyant la réponse finale vers la sortie attendue (log, interface, output)
Priorité : 5
Auteur : Matthieu
"""

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.transmetteur")


class TransmetteurPlugin(BasePlugin):
    meta = Meta(
        name="transmetteur",
        priority=5,
        version="1.0",
        author="Matthieu"
    )

    async def run(self, ctx: Context) -> Context:
        final = ctx.get("final_response", "")
        output = f"[Réponse finale du noyau] : {final}"

        ctx["output_message"] = output
        ctx.setdefault("plugins_log", []).append("Transmetteur : réponse envoyée.")
        logger.info(f"[transmetteur] {output}")

        return ctx
