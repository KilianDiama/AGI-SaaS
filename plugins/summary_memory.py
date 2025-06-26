import logging
from typing import Any, Dict, List

import pandas as pd

from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.summary_memory")

class SummaryMemoryPlugin(BasePlugin):
    meta = Meta(
        name="summary_memory",
        priority=-975,    # juste après export_memory si tu l'ajoutes
        version="1.0",
        author="Matt & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        memoire: List[Dict[str, Any]] = ctx.get("memoire_long_terme", [])
        if not memoire:
            logger.warning("[summary_memory] Pas de mémoire long terme.")
            ctx.setdefault("plugins_log", []).append("SummaryMemoryPlugin : pas de mémoire.")
            return ctx

        try:
            # 1) Charge dans un DataFrame
            df = pd.DataFrame(memoire)

            # 2) Coup d’œil global : nombre d’entrées et types
            total = len(df)
            types = df['type'].value_counts().to_dict() if 'type' in df else {}

            # 3) Ajoute quelques stats temporelles si tu as un timestamp
            if 'timestamp' in df:
                df['ts'] = pd.to_datetime(df['timestamp'])
                first = df['ts'].min()
                last  = df['ts'].max()
                span  = last - first
            else:
                first = last = span = None

            # 4) Formate le résumé
            résumé = [
                f"🔸 Entrées mémoire long terme : {total}",
                f"🔸 Répartition par type : {types}",
            ]
            if first is not None:
                résumé += [
                    f"🔸 Première entrée : {first.isoformat()}",
                    f"🔸 Dernière entrée  : {last.isoformat()}",
                    f"🔸 Période totale  : {span}"
                ]

            # 5) Injecte dans le contexte
            ctx["memory_summary"] = "\n".join(résumé)
            ctx.setdefault("plugins_log", []).append(
                "SummaryMemoryPlugin : résumé généré."
            )
            logger.info("[summary_memory] Résumé mémoire injecté.")

        except Exception as e:
            logger.error(f"[summary_memory] Erreur : {e}")
            ctx.setdefault("plugins_log", []).append(
                f"SummaryMemoryPlugin : erreur → {e}"
            )

        return ctx
