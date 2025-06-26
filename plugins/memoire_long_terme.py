# plugins/memoire_long_terme.py

from noyau_core import BasePlugin, Context, Meta
import logging
import os
import json
from datetime import datetime

logger = logging.getLogger("plugin.memoire_long_terme")

MEM_FILE = "memoire_long_terme.json"

class MemoireLongTermePlugin(BasePlugin):
    meta = Meta(
        name="memoire_long_terme",
        priority=-980,  # Tôt dans le cycle
        version="1.0",
        author="Toi & GPT"
    )

    def charger_memoire(self) -> dict:
        if not os.path.exists(MEM_FILE):
            return {}
        with open(MEM_FILE, "r") as f:
            return json.load(f)

    def sauvegarder(self, mem: dict):
        with open(MEM_FILE, "w") as f:
            json.dump(mem, f, indent=2)

    async def run(self, ctx: Context) -> Context:
        mem = self.charger_memoire()
        action = ctx.get("memoire_action", "read")
        cle = ctx.get("memoire_cle")
        contenu = ctx.get("memoire_valeur")
        tags = ctx.get("memoire_tags", [])

        if action == "write" and cle and contenu:
            mem[cle] = {
                "contenu": contenu,
                "timestamp": datetime.utcnow().isoformat(),
                "tags": tags
            }
            self.sauvegarder(mem)
            ctx["memoire_resultat"] = f"Enregistré sous {cle}"

        elif action == "read" and cle:
            ctx["memoire_resultat"] = mem.get(cle, {}).get("contenu", None)

        elif action == "search" and tags:
            resultats = []
            for val in mem.values():
                if all(tag in val.get("tags", []) for tag in tags):
                    resultats.append(val["contenu"])
            ctx["memoire_resultat"] = resultats

        ctx.setdefault("plugins_log", []).append(f"MemoireLongTermePlugin : action={action}")
        return ctx
