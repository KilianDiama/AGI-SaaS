# plugins/orchestrateur_llm.py

from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.orchestrateur_llm")

class OrchestrateurLLMPlugin(BasePlugin):
    meta = Meta(
        name="orchestrateur_llm",
        priority=-992,      # Juste après InputPlugin
        version="3.0",
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        # 1. Chargement des éléments mémoire & objectif
        mem         = ctx.get("memoire_contextuelle", "")
        objectif    = ctx.get("objectif", {}).get("but", "répondre à une question")
        tache       = ctx.get("tache_courante", "analyse de la demande")
        web_infos   = ctx.get("web_infos", "")
        reflexion   = ctx.get("reflexion_interne", "")
        resultats   = []

        # 2. Extraction message utilisateur prioritaire
        user_msg = ""
        messages = ctx.get("payload", {}).get("messages", [])
        if messages:
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    user_msg = msg.get("content", "").strip()
                    break

        # 3. Fallback si vide
        if not user_msg:
            user_msg = ctx.get("message", "").strip()

        if not user_msg:
            logger.warning("[orchestrateur_llm] Message utilisateur vide — injection d’un prompt générique.")
            user_msg = "(Aucune demande utilisateur explicite détectée.)"

        # 4. Ajout d'autres infos du contexte
        if "calc_result" in ctx:
            resultats.append(f"🧮 Résultat calculé : {ctx['calc_result']}")
        if "résumé" in ctx:
            resultats.append(f"📝 Résumé extrait : {ctx['résumé']}")
        if "structured_query" in ctx:
            resultats.append(f"🔎 Requête structurée : {ctx['structured_query']}")
        if "infos_extraites" in ctx:
            resultats.append(f"📊 Données extraites : {ctx['infos_extraites']}")

        role    = ctx.get("role", "assistant expert")
        ton     = ctx.get("ton", "neutre")
        style   = ctx.get("style", "clair et structuré")

        # 5. Construction finale du prompt
        prompt = f"""Tu es un {role}.
Ton : {ton}
Style : {style}

Objectif global : {objectif}
Étape actuelle : {tache}

Réflexion interne :
{reflexion or "N/A"}

Historique :
{mem or "Aucune mémoire disponible."}

Données utiles :
{web_infos or "Aucune information web disponible."}
{chr(10).join(resultats)}

Message utilisateur :
{user_msg}

🧠 Réponds de façon logique, cohérente, structurée et pertinente pour atteindre l’objectif.
"""

        # 6. Injection dans le contexte
        ctx["llm_prompt"] = prompt
        ctx["llm_prompt_locked"] = True
        ctx.setdefault("plugins_log", []).append("OrchestrateurLLM : prompt complet injecté.")
        logger.info("[orchestrateur_llm] Prompt généré et verrouillé.")

        return ctx
