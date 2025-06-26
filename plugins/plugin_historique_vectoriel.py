# plugins/plugin_historique_vectoriel.py

"""
Plugin : historique_vectoriel
Rôle   : Encode chaque message et objectif dans l’espace vectoriel, retrouve les contextes les plus proches
Priorité : -27 (avant raisonnement, après relation_contextuelle)
Auteur  : Toi + GPT
"""

import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.historique_vectoriel")

class HistoriqueVectorielPlugin(BasePlugin):
    meta = Meta(
        name="historique_vectoriel",
        priority=-27,
        version="1.1",  # ← version corrigée
        author="Toi + GPT"
    )

    archives = []
    vecteurs = []
    vectorizer = TfidfVectorizer()

    async def run(self, ctx: Context) -> Context:
        log = ctx.setdefault("plugins_log", [])
        message = ctx.get("message", "")
        objectif = ctx.get("objectif_general", "")
        cycle_id = ctx.get("cycle_id")

        # Sécurité typage
        if not isinstance(message, str):
            message = str(message)
        if not isinstance(objectif, str):
            objectif = str(objectif)

        texte_complet = f"{message} {objectif}".strip()

        if not texte_complet:
            ctx["vecteurs_proches"] = []
            log.append("HistoriqueVectorielPlugin : rien à encoder (message + objectif vides).")
            return ctx

        try:
            documents = [a["texte"] for a in self.archives] + [texte_complet]
            vects = self.vectorizer.fit_transform(documents)

            if vects.shape[0] > 1:
                nouveau_vecteur = vects[-1].toarray()[0]
                anciens = vects[:-1].toarray()
                similarites = [self.cos_sim(nouveau_vecteur, v) for v in anciens]

                liens = sorted([
                    {"cycle_id": a["cycle_id"], "sim": round(s, 2), "texte": a["texte"]}
                    for a, s in zip(self.archives, similarites) if s > 0.4
                ], key=lambda x: -x["sim"])

                ctx["vecteurs_proches"] = liens
                log.append(f"HistoriqueVectorielPlugin : {len(liens)} souvenirs vectoriels pertinents retrouvés.")
                logger.info(f"[historique_vectoriel] Contextes similaires : {liens}")
            else:
                ctx["vecteurs_proches"] = []
                log.append("HistoriqueVectorielPlugin : premier encodage effectué.")
        except ValueError as e:
            ctx["vecteurs_proches"] = []
            log.append(f"HistoriqueVectorielPlugin : erreur d’encodage TF-IDF ({str(e)}).")
            logger.warning(f"[historique_vectoriel] Erreur TF-IDF : {str(e)}")

        # Ajout à la mémoire vectorielle
        self.archives.append({
            "cycle_id": cycle_id,
            "texte": texte_complet
        })

        return ctx

    def cos_sim(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
