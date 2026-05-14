# vector_store.py
# Responsibility: Manage ChromaDB collections — upsert and query.
# Owner: Engineer D (shared util)
#
# TODO: class VectorStore
#   __init__(self, collection_name: str, persist_dir: str = "./chroma_db")
#     - Init chromadb.PersistentClient
#     - Get or create collection with name=collection_name
#
#   upsert(self, chunks: list[dict]) -> None
#     - chunks must have: text, embedding, source, chunk_index
#     - Build ids, embeddings, documents, metadatas lists
#     - Call self.collection.upsert(...)
#
#   query(self, query_embedding: list[float], top_k: int = 3) -> list[dict]
#     - Call self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
#     - Return list of { "text": str, "source": str, "distance": float }
#
#   count(self) -> int
#     - Return self.collection.count()


class VectorStore:
    def __init__(self, collection_name: str, persist_dir: str = "./chroma_db"):
        pass

    def upsert(self, chunks: list) -> None:
        pass

    def query(self, query_embedding: list, top_k: int = 3) -> list:
        pass

    def count(self) -> int:
        pass
