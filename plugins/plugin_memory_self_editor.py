# plugins/plugin_memory_self_editor.py
from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.memory_self_editor")

class PluginMemorySelfEditor(BasePlugin):
    meta = Meta(
        name="plugin_memory_self_editor",
        version="1.0",
        priority=85.0,  # après les mémoires mais avant planificateurs
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        memoire_profonde = ctx.get("memoire_profonde", {})
        if not memoire_profonde:
            ctx.setdefault("plugins_log", []).append("PluginMemorySelfEditor : pas de mémoire à éditer.")
            return ctx

        new_memoire = {}
        for key, bloc in memoire_profonde.items():
            résumé = bloc.get("résumé", "")
            if not résumé:
                continue

            prompt = (
                f"Voici un souvenir : « {résumé} »\n"
                "Peux-tu reformuler ce souvenir de façon plus concise, précise, et utile pour le futur ?"
            )

            try:
                from plugins.utils.llm_call import call_llm_main
                reformulé = await call_llm_main(ctx, prompt)
                new_memoire[key] = {
                    **bloc,
                    "résumé": reformulé.strip(),
                    "version": "optimisé"
                }
                ctx.setdefault("plugins_log", []).append(f"MemorySelfEditor : bloc {key} optimisé.")
            except Exception as e:
                logger.warning(f"[PluginMemorySelfEditor] Erreur pour {key} : {e}")

        if new_memoire:
            ctx["memoire_profonde"] = new_memoire

        return ctx
