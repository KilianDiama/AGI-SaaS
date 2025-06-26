# plugins/plugin_memoire_strategique.py
from noyau_core import BasePlugin, Context, Meta
import json, hashlib
import logging

logger = logging.getLogger("plugin.memoire_strategique")

class PluginMemoireStrategique(BasePlugin):
    meta = Meta(
        name="plugin_memoire_strategique",
        version="1.0",
        priority=50.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        plan = ctx.get("plan")
        score = ctx.get("self_eval_score", {}).get("note", 0)
        objectif = ctx.get("objectif", {}).get("but", "inconnu")
        contexte = ctx.get("memoire_contextuelle", "")
        cycle_id = ctx.get("cycle_id", "N/A")

        if not plan:
            ctx.setdefault("plugins_log", []).append("PluginMemoireStrategique : aucun plan.")
            return ctx

        plan_hash = hashlib.sha256(json.dumps(plan).encode()).hexdigest()

        nouvelle_entree = {
            "objectif": objectif,
            "plan": plan,
            "hash": plan_hash,
            "note": score,
            "contexte": contexte,
            "cycle_id": cycle_id,
        }

        memoire = ctx.setdefault("memoire_strategique", {})
        memoire[plan_hash] = nouvelle_entree

        ctx.setdefault("plugins_log", []).append(f"PluginMemoireStrategique : plan sauvegardé (score={score}).")
        return ctx
