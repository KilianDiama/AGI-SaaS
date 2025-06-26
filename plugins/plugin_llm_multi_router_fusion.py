# plugins/plugin_llm_multi_router_fusion.py

from noyau_core import BasePlugin, Context, Meta
import subprocess
import logging
import json

logger = logging.getLogger("plugin.llm_multi_router_fusion")

class PluginLLMMultiRouterFusion(BasePlugin):
    meta = Meta(
        name="plugin_llm_multi_router_fusion",
        version="1.0",
        priority=5.0,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt = ctx.get("llm_prompt", "")
        if not prompt.strip():
            ctx.setdefault("plugins_log", []).append("plugin_llm_multi_router_fusion : prompt manquant.")
            return ctx

        # Liste des modèles disponibles — adapte-la à ce que tu as vu dans `ollama list`
        models = [
            "llava", "openhermes", "dolphin-mixtral", "wizardcoder", "tinyllama",
            "neural-chat", "codellama", "phi3", "gemma", "mistral", "llama3", "orca-mini"
        ]

        reponses_valides = {}
        erreurs = []

        for model in models:
            try:
                logger.info(f"[plugin_llm_multi_router_fusion] Appel modèle {model}")
                result = subprocess.run(
                    ["ollama", "run", model],
                    input=prompt.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=15
                )
                sortie = result.stdout.decode().strip()
                if sortie and "error" not in sortie.lower():
                    reponses_valides[model] = sortie
                else:
                    erreurs.append((model, sortie or result.stderr.decode()))
            except Exception as e:
                erreurs.append((model, str(e)))

        # Sélection de la meilleure réponse
        if reponses_valides:
            # Tu peux affiner ici : par longueur, mot-clé, modèle préféré…
            meilleur_model, meilleure_reponse = sorted(reponses_valides.items(), key=lambda x: len(x[1]), reverse=True)[0]
            ctx["llm_response"] = meilleure_reponse
            ctx["model_utilisé"] = meilleur_model
            ctx.setdefault("plugins_log", []).append(f"plugin_llm_multi_router_fusion : réponse de {meilleur_model} utilisée ✅")
        else:
            ctx["llm_response"] = "❌ Aucun modèle n'a pu générer de réponse."
            ctx.setdefault("plugins_log", []).append("plugin_llm_multi_router_fusion : toutes les tentatives ont échoué ❌")
            for err in erreurs:
                logger.warning(f"[plugin_llm_multi_router_fusion] Erreur modèle {err[0]} : {err[1][:120]}...")

        return ctx
