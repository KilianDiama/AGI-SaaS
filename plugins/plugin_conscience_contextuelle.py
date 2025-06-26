from noyau_core import BasePlugin, Context, Meta
import logging

logger = logging.getLogger("plugin.conscience_contextuelle")

class PluginConscienceContextuelle(BasePlugin):
    meta = Meta(
        name="plugin_conscience_contextuelle",
        version="1.0",
        priority=2.0,  # Juste avant la formulation finale
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        sections = []

        # Mission
        objectif = ctx.get("objectif", {}).get("but", "non défini")
        sections.append(f"🎯 **Objectif actuel** : {objectif}")

        # Utilisateur
        user_email = ctx.get("user_email", "anonyme")
        plan = ctx.get("plan", [])
        sections.append(f"👤 **Utilisateur** : {user_email}")

        # Mémoire courte
        memoire = ctx.get("memoire_contextuelle", "").strip()
        if memoire:
            sections.append(f"🧠 **Mémoire contextuelle** : {memoire[:200]}{'...' if len(memoire) > 200 else ''}")
        else:
            sections.append("🧠 **Mémoire contextuelle** : vide")

        # Plan en cours
        if plan:
            plan_status = "\n".join([f"- {step['étape']} [{step['status']}]" for step in plan])
            sections.append(f"📋 **Plan actif** :\n{plan_status}")
        else:
            sections.append("📋 **Plan actif** : Aucun")

        # Tâche courante
        task = ctx.get("tache_courante", "non définie")
        sections.append(f"🔄 **Tâche en cours** : {task}")

        # Mode
        mode = ctx.get("performance_mode", "standard")
        sections.append(f"⚙️ **Mode de performance** : {mode}")

        # Injection finale
        conscience = "\n\n".join(sections)
        ctx["conscience_contextuelle"] = conscience
        ctx.setdefault("plugins_log", []).append("plugin_conscience_contextuelle : conscience générée.")
        logger.info(f"[conscience] État global injecté:\n{conscience}")

        return ctx
