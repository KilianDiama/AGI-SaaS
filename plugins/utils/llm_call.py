from noyau_core import Context
import ollama

async def call_llm_main(ctx: Context, prompt: str) -> str:
    try:
        model = ctx.get("llm_model", "llama3")
        temperature = ctx.get("llm_config", {}).get("temperature", 0.7)
        max_tokens = ctx.get("llm_config", {}).get("max_tokens", 1024)

        # Appel à l'API locale d'Ollama
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        return response["message"]["content"].strip()

    except Exception as e:
        ctx.setdefault("plugins_log", []).append(f"call_llm_main : erreur → {e}")
        return "⚠️ Erreur lors de l'appel LLM via Ollama."
