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


def get_embedder():
    pass


def embed_chunks(chunks: list, embedder) -> list:
    pass
