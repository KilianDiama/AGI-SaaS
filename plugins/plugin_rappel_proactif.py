from datetime import datetime, timedelta
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.rappel_proactif")

class PluginRappelProactif(BasePlugin):
    meta = Meta(
        name="plugin_rappel_proactif",
        version="1.0",
        priority=1.6,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        user_id = ctx.get("user", {}).get("id", "anonymous")
        objectifs = ctx.get("objectifs_persistants", [])
        now = datetime.utcnow()

        rappels = []

        for obj in objectifs:
            ts_str = obj.get("timestamp")
            if not ts_str:
                continue
            try:
                ts = datetime.fromisoformat(ts_str)
                age = now - ts

                # Critère : objectif vieux de +48h, encore actif
                if age > timedelta(hours=48) and obj.get("état") != "terminé":
                    rappels.append(f"⏰ Tu avais un objectif : **{obj['but']}** il y a {age.days} jour(s). Souhaites-tu y revenir ?")

            except Exception as e:
                logger.warning(f"[rappel_proactif] Problème de date : {e}")

        if rappels:
            ctx["rappel_proactif"] = "\n\n".join(rappels)
            ctx.setdefault("plugins_log", []).append(f"PluginRappelProactif : {len(rappels)} rappel(s) généré(s).")
            logger.info(f"[rappel_proactif] {len(rappels)} rappel(s) pour {user_id}")
        else:
            ctx.setdefault("plugins_log", []).append("PluginRappelProactif : aucun rappel utile détecté.")

        return ctx
