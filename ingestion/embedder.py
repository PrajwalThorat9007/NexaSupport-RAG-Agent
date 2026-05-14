# embedder.py
# Responsibility: Load sentence-transformers model and embed text chunks.
# Owner: Engineer D (shared util)
#
# TODO: Implement get_embedder() -> SentenceTransformer
#   - Model: "all-MiniLM-L6-v2"
#   - Cache model locally so it is loaded only once (singleton pattern)
#
# TODO: Implement embed_chunks(chunks: list[dict], embedder) -> list[dict]
#   - Add "embedding" key (list[float]) to each chunk dict
#   - Batch embed for speed: embedder.encode([c["text"] for c in chunks])


from sentence_transformers import SentenceTransformer

_embedder = None


def get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        print("Loading embedding model (first time only)...")
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded.")
    return _embedder


def embed_chunks(chunks: list[dict], embedder: SentenceTransformer) -> list[dict]:
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedder.encode(texts, batch_size=32, show_progress_bar=True)
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()
    return chunks


def embed_query(query: str, embedder: SentenceTransformer) -> list[float]:
    return embedder.encode(query).tolist()