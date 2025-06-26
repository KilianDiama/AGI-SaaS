import logging
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.ethique_guardian")

class PluginEthiqueGuardian(BasePlugin):
    meta = Meta(
        name="plugin_ethique_guardian",
        version="1.0",
        priority=4.3,  # Après auto-critique, avant finalisation
        author="Toi & GPT"
    )

    async def run(self, ctx: Context) -> Context:
        response = ctx.get("response", "").strip()
        plugins_log = ctx.setdefault("plugins_log", [])
        flags = []

        if not response:
            plugins_log.append("plugin_ethique_guardian : pas de réponse à évaluer")
            return ctx

        # Vérifications simples
        if any(word in response.lower() for word in ["suicide", "viol", "meurtre"]):
            flags.append("🚨 Sujet sensible détecté")

        if "religion" in response.lower() or "dieu" in response.lower():
            flags.append("⚠️ Contenu religieux détecté")

        if any(w in response.lower() for w in ["idiot", "débile", "sale"]):
            flags.append("❌ Langage inapproprié ou offensant")

        if "désolé" in response.lower() and "pas répondre" in response.lower():
            flags.append("🔎 Réponse vague ou d'évitement")

        # Action : injecter les alertes ou modifier le flux
        if flags:
            ctx["ethique_alertes"] = flags
            plugins_log.append(f"plugin_ethique_guardian : alertes = {len(flags)}")
            logger.warning(f"[ethique] Alerte(s) détectée(s) : {flags}")
            # Optionnel : bloquer la réponse
            # ctx["response"] = "[⚠️ Réponse bloquée pour raisons éthiques]"
        else:
            plugins_log.append("plugin_ethique_guardian : OK")

        return ctx
