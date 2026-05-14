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


import chromadb
from chromadb.config import Settings


class VectorStore:
    def __init__(self, collection_name: str, persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Collection '{collection_name}' ready — {self.count()} docs stored.")

    def upsert(self, chunks: list[dict]) -> None:
        if not chunks:
            return
        ids = [f"{c['source']}__chunk{c['chunk_index']}" for c in chunks]
        embeddings = [c["embedding"] for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks]

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Upserted {len(chunks)} chunks into '{self.collection.name}'.")

    def query(self, query_embedding: list[float], top_k: int = 3) -> list[dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        output = []
        for i in range(len(results["documents"][0])):
            output.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i]
            })
        return output

    def count(self) -> int:
        return self.collection.count()