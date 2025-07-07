from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

class VectorDB:
    async def similarity_search(self, query: str, corpus: list, top_k: int = 1):
        q_emb = model.encode(query, convert_to_tensor=True)
        c_emb = model.encode(corpus, convert_to_tensor=True)
        hits = util.semantic_search(q_emb, c_emb, top_k=top_k)[0]
        return [corpus[h['corpus_id']] for h in hits]