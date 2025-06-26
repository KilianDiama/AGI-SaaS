"""
Plugin : temps_subjectif
Rôle : Générer une perception intérieure du temps basé sur la charge et l’état mental
Priorité : 6
Auteur : AGI_Matt & GPT
"""

from noyau_core import BasePlugin, Context, Meta
import logging
from datetime import datetime

logger = logging.getLogger("plugin.temps_subjectif")

class TempsSubjectifPlugin(BasePlugin):
    meta = Meta(
        name="temps_subjectif",
        priority=6,
        version="1.0",
        author="AGI_Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        mémoire_temps = ctx.setdefault("mémoire_temps_subjectif", [])
        now = datetime.utcnow()

        dernier_cycle = mémoire_temps[-1]["timestamp"] if mémoire_temps else now
        ecart = (now - dernier_cycle).total_seconds()

        charge = len(ctx.get("plugins_log", [])) + len(ctx.get("llm_response", ""))
        vitesse = "ralenti" if charge < 300 else "normal" if charge < 600 else "accéléré"

        perception = {
            "timestamp": now,
            "vitesse_perçue": vitesse,
            "durée_ressentie": f"{round(ecart * (1.5 if vitesse == 'ralenti' else 0.7 if vitesse == 'accéléré' else 1.0), 2)}s",
            "état": ctx.get("centre_de_gravite", "non défini")
        }

        mémoire_temps.append(perception)
        ctx["temps_subjectif"] = perception

        plugins_log.append(f"TempsSubjectifPlugin : vitesse = {vitesse}, durée = {perception['durée_ressentie']}")
        logger.info(f"[temps_subjectif] {perception}")

        return ctx
