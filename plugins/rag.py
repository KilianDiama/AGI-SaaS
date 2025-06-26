# plugins/rag.py
import os, pickle, logging
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
from noyau_core import BasePlugin, Context, Meta

logger = logging.getLogger("plugin.rag")

class RAGPlugin(BasePlugin):
    meta = Meta(name="rag", priority=-945, version="1.0", author="Matt")

    async def before(self, ctx: Context) -> None:
        # charge index FAISS et embeddings (pickles)
        idx_path = "faiss.index"
        emb_path = "embeddings.pkl"
        if os.path.exists(idx_path) and os.path.exists(emb_path):
            self.index = faiss.read_index(idx_path)
            self.embeddings = pickle.load(open(emb_path, "rb"))
            self.ids = list(self.embeddings.keys())
            # tokenizer/model commun
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
            self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        else:
            self.index = None

    async def run(self, ctx: Context) -> Context:
        if not self.index:
            logger.warning("rag → index introuvable, skip")
            return ctx

        query = ctx["payload"].get("message", "")
        # embed query
        inputs = self.tokenizer(query, return_tensors="pt", padding=True)
        vec = self.model(**inputs).last_hidden_state.mean(dim=1).detach().numpy().astype(np.float32)
        D, I = self.index.search(vec, k=3)
        docs = [self.ids[i] for i in I[0]]
        ctx["rag_documents"] = docs
        ctx.setdefault("plugins_log", []).append(f"{self.meta.name} : {len(docs)} docs récupérés")
        # on peut injecter ces docs dans le prompt
        ctx["llm_prompt"] = ctx.get("llm_prompt", "") + "\n\nDocuments:\n" + "\n".join(docs)
        return ctx
