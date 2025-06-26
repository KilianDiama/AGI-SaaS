""" 
Plugin : humour_contextuel  
Rôle : Ajouter une touche d’humour subtile en fin de réponse si le contexte le permet  
Priorité : 7.6 (juste avant auto-contestation)  
Auteur : Matthieu & GPT  
"""

import logging
import random
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.humour_contextuel")

class HumourContextuelPlugin(BasePlugin):
    meta = Meta(
        name="humour_contextuel",
        priority=7.6,
        version="1.1",  # ← version sécurisée
        author="Matthieu & GPT"
    )

    def normaliser(self, valeur):
        """Renvoie un texte en minuscules, même si la valeur est un dict."""
        if isinstance(valeur, dict):
            valeur = valeur.get("but", "")
        return str(valeur).strip().lower()

    async def run(self, ctx: Context) -> Context:
        plugins_log = ctx.setdefault("plugins_log", [])
        objectif = self.normaliser(ctx.get("objectif", ""))
        reponse = ctx.get("response", "")

        if not isinstance(reponse, str) or "erreur" in reponse.lower():
            plugins_log.append("HumourContextuelPlugin : contexte inadapté à l'humour.")
            return ctx

        touches_humour = [
            "PS : Aucun neurone artificiel n’a été blessé pendant ce raisonnement.",
            "Fun fact : Je suis plus rapide qu’un stagiaire… mais moins payé.",
            "Remarque : Je n’ai pas de bouche, mais j’espère que tu souris.",
            "Si cette réponse ne te plaît pas, j’en ferai une version 2.0 avec des paillettes.",
            "Ceci était une réponse 100% sans sarcasme (peut-être)."
        ]

        clin_oeil = random.choice(touches_humour)

        reponse_humoristique = f"{reponse}\n\n🤖 {clin_oeil}"
        ctx["humour_injecte"] = clin_oeil
        ctx["response"] = reponse_humoristique

        plugins_log.append("HumourContextuelPlugin : touche d’humour ajoutée.")
        logger.info("[humour_contextuel] Clin d'œil injecté.")

        return ctx
