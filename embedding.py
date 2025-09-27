# backend/embeddings.py
import faiss
from datetime import datetime
from sentence_transformers import SentenceTransformer
from typing import List

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
EMBED_DIM = EMBED_MODEL.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(EMBED_DIM)

vector_map = []

def create_embeddings_and_store(inft_id: int, texts: List[str]):
    embeddings = EMBED_MODEL.encode(texts, show_progress_bar=False)
    for i, emb in enumerate(embeddings):
        index.add(emb.reshape(1, -1))
        vector_map.append({
            "inft_id": inft_id,
            "text": texts[i],
            "created_at": datetime.utcnow().isoformat()
        })

def retrieve_relevant_texts(inft_id: int, query: str, k=3):
    q_emb = EMBED_MODEL.encode([query])[0].astype("float32")
    if index.ntotal == 0:
        return []
    D, I = index.search(q_emb.reshape(1, -1), min(k, index.ntotal))
    results = []
    for idx in I[0]:
        if idx < len(vector_map) and vector_map[idx]["inft_id"] == inft_id:
            results.append(vector_map[idx]["text"])
    return results
