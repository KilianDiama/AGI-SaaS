# plugins/plugin_traceur_meta_apprentissage.py

from noyau_core import BasePlugin, Context, Meta
import time

class PluginTraceurMetaApprentissage(BasePlugin):
    meta = Meta(
        name="plugin_traceur_meta_apprentissage",
        version="1.0",
        priority=2.8,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        trace = ctx.setdefault("meta_trace_apprentissage", [])
        actions = ctx.get("actions_appliquees", [])
        note = ctx.get("evaluation_reponse", {}).get("note", None)
        cycle_id = ctx.get("cycle_id", f"cycle_{int(time.time())}")

        if actions and note is not None:
            trace_entry = {
                "cycle": cycle_id,
                "note": note,
                "actions": actions,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "tonalite": ctx.get("tonalite_utilisateur", "unknown"),
                "intention": ctx.get("intention", "unknown"),
                "objectif": ctx.get("objectif", {}).get("but", "unknown")
            }
            trace.append(trace_entry)

            # Limiter à 20 derniers cycles
            if len(trace) > 20:
                trace.pop(0)

            ctx["plugins_log"].append(f"PluginTraceurMetaApprentissage : trace ajoutée (note={note}, actions={actions})")

        return ctx
