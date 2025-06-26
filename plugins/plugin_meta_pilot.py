class PluginMetaPilot:
    def __init__(self):
        self.id = "plugin_meta_pilot"
        self.description = "Analyse globale du pipeline LLM pour détecter les inefficacités et proposer des améliorations"

    def execute(self, contexte):
        plugins_log = contexte.get("plugins_log", [])
        total_plugins = len(plugins_log)
        utiles = [p for p in plugins_log if "injectée" in p or "ajoutée" in p or "réalisée" in p]
        erreurs = [p for p in plugins_log if "erreur" in p.lower() or "échec" in p.lower()]
        ratio_utilite = len(utiles) / total_plugins if total_plugins else 0

        feedback = {
            "total_plugins": total_plugins,
            "utiles": len(utiles),
            "erreurs": len(erreurs),
            "ratio_utilite": round(ratio_utilite, 2),
            "suggestion": ""
        }

        if ratio_utilite < 0.4:
            feedback["suggestion"] = "🔧 Moins de 40% des plugins ont été utiles. Réévaluer le pipeline de cycle."
        elif erreurs:
            feedback["suggestion"] = f"⚠️ {len(erreurs)} erreurs détectées. Ajouter une vérification de robustesse."
        else:
            feedback["suggestion"] = "✅ Pipeline stable. Aucun ajustement immédiat requis."

        # Injection dans le contexte
        contexte["meta_pilot_feedback"] = feedback
        return f"{self.id} : feedback sur pipeline généré."

