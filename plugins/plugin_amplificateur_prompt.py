from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.amplificateur_prompt")

class PluginAmplificateurPrompt(BasePlugin):
    meta = Meta(
        name="plugin_amplificateur_prompt",
        version="1.0",
        priority=4.5,
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        prompt_brut = ctx.get("llm_prompt", "")
        modele = ctx.get("llm_model", "llm")
        intention = ctx.get("intention", "")
        objectif = ctx.get("objectif", {}).get("but", "")
        resume = ctx.get("memoire_contextuelle", "")

        # Enrichissement du prompt de manière ciblée
        amplifications = []

        if "réécris" in prompt_brut or "améliore" in prompt_brut:
            amplifications.append("✅ Amélioration du style activée.")
        if resume and len(resume) > 30:
            amplifications.append("🧠 Résumé contextuel injecté pour plus de cohérence.")
            prompt_brut = f"[Résumé : {resume}]\n\n{prompt_brut}"

        if intention.lower() in ["créatif", "histoire", "scénario"]:
            prompt_brut = "Tu es un assistant créatif et inspirant.\n\n" + prompt_brut
        elif intention.lower() in ["analyse", "logique", "synthèse"]:
            prompt_brut = "Tu es un assistant rigoureux et méthodique.\n\n" + prompt_brut

        if modele == "mistral":
            prompt_brut = prompt_brut.replace("Réécris", "Réécris clairement pour Mistral :")
        elif modele == "llama3":
            prompt_brut += "\n\nUtilise un style fluide et structuré."

        ctx["llm_prompt"] = prompt_brut
        ctx.setdefault("plugins_log", []).append("PluginAmplificateurPrompt : prompt enrichi.")
        logger.info(f"[amplificateur_prompt] Prompt enrichi avec : {amplifications}")

        return ctx
