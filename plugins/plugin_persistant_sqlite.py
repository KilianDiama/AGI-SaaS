# plugins/plugin_persistant_sqlite.py

"""
Plugin : persistant_sqlite
Rôle   : Sauvegarde/restaure les données du contexte utilisateur via SQLite
Priorité : -98 (juste après identité)
Auteur  : Toi + GPT
"""

import sqlite3
import json
from noyau_core import BasePlugin, Context, Meta

class PersistantSQLitePlugin(BasePlugin):
    meta = Meta(
        name="persistant_sqlite",
        priority=-98,
        version="1.0",
        author="Toi + GPT"
    )

    DB_PATH = "data/contexte.sqlite"

    def _ensure_db(self):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS contextes (
                user_id TEXT PRIMARY KEY,
                data TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _save(self, user_id, data):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute("REPLACE INTO contextes (user_id, data) VALUES (?, ?)", (user_id, json.dumps(data)))
        conn.commit()
        conn.close()

    def _load(self, user_id):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data FROM contextes WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        return json.loads(row[0]) if row else {}

    async def run(self, ctx: Context) -> Context:
        self._ensure_db()
        user_id = ctx.get("identite_utilisateur", {}).get("user_id", "anonyme")

        if ctx.get("sauver_contexte", False):
            self._save(user_id, ctx)
        else:
            ancien_ctx = self._load(user_id)
            ctx.update({**ancien_ctx, **ctx})

        return ctx
