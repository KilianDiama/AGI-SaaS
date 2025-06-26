# api/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from noyau_core import charger_plugins_complet

app = FastAPI()
plugins = charger_plugins_complet()

# Structure du message entrant
class MessageRequest(BaseModel):
    message: str
    user_id: str
    session_id: str

@app.post("/think")
async def think(req: MessageRequest):
    # Contexte initial du cycle
    ctx = {
        "message": req.message.strip(),
        "user_id": req.user_id,
        "session_id": req.session_id,
        "cycle_id": f"{req.user_id[:4]}-{req.session_id[:4]}",
        "llm_responses": [],
        "log_cognitif": {}
    }

    # Exécution de tous les plugins
    for plugin in plugins:
        if hasattr(plugin, "run"):
            try:
                result = await plugin.run(ctx)
                if result:
                    ctx.update(result)
            except Exception as e:
                ctx.setdefault("log_cognitif", {})[f"{plugin.__class__.__name__}_error"] = str(e)

    # Fallback LLM si aucune réponse directe
    if not ctx.get("llm_response") and ctx.get("llm_responses"):
        for r in ctx["llm_responses"]:
            if isinstance(r, str) and "Exception" not in r:
                parts = r.split('\n', 1)
                ctx["llm_response"] = parts[1].strip() if len(parts) > 1 else r.strip()
                ctx.setdefault("log_cognitif", {})["fallback_used"] = True
                break

    # Sortie API
    return {
        "reponse": ctx.get("llm_response", "[Aucune réponse générée]"),
        "log": ctx.get("log_cognitif", {}),
        "meta": {
            "objectif": ctx.get("objectif_general"),
            "concepts": [c["nom"] for c in ctx.get("concepts_crees", [])] if ctx.get("concepts_crees") else [],
            "symboles": ctx.get("symboles_expressifs", []),
            "etat": ctx.get("noyau_conscient", "")
        }
    }
