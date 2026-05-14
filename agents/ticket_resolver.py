# ticket_resolver.py  —  UC-1
# Responsibility: Given a new support ticket, retrieve similar past resolutions
#                 and generate a suggested reply draft with confidence score.
# Owner: Engineer A
#
# TODO: class TicketResolver
#   __init__(self, vector_store: VectorStore, embedder, groq_client)
#     - Store references to shared vector_store, embedder, groq_client
#     - Load prompt template from prompts/ticket_resolver.txt
#
#   resolve(self, ticket_text: str, top_k: int = 3) -> dict
#     - Embed ticket_text using embedder
#     - Query vector_store for top_k similar chunks
#     - Build prompt: inject retrieved chunks as context
#     - Call Groq API (llama3-8b-8192)
#     - Return: { "draft_reply": str, "sources": list[str], "confidence": float }
#
# Confidence score logic:
#   - Use mean cosine similarity of retrieved chunks as proxy
#   - High similarity (< 0.3 distance) → high confidence


# agents/ticket_resolver.py — UC-1
# Engineer: E1 Prajwal

import os
from groq import Groq
from dotenv import load_dotenv
from ingestion.embedder import get_embedder, embed_query
from ingestion.vector_store import VectorStore

load_dotenv()


class TicketResolver:
    def __init__(self):
        self.embedder = get_embedder()
        self.store = VectorStore(
            collection_name="nexasupport",
            persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        )
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

        prompt_path = os.path.join("prompts", "ticket_resolver.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def resolve(self, ticket_text: str, top_k: int = 3) -> dict:
        # Step 1 — embed the incoming ticket
        query_embedding = embed_query(ticket_text, self.embedder)

        # Step 2 — retrieve top-k similar chunks from ChromaDB
        results = self.store.query(query_embedding, top_k=top_k)

        if not results:
            return {
                "draft_reply": "No relevant context found. Please escalate to Tier 2 support.",
                "sources": [],
                "confidence": 0.0
            }

        # Step 3 — build context block from retrieved chunks
        context_parts = []
        sources = []
        for r in results:
            context_parts.append(r["text"])
            sources.append(r["source"])

        context = "\n\n---\n\n".join(context_parts)

        # Step 4 — fill prompt template
        prompt = self.prompt_template.format(
            context=context,
            ticket_text=ticket_text
        )

        # Step 5 — call Groq LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )

        reply = response.choices[0].message.content.strip()

        # Step 6 — calculate confidence from distances
        avg_distance = sum(r["distance"] for r in results) / len(results)
        if avg_distance < 0.3:
            confidence = 1.0
        elif avg_distance < 0.6:
            confidence = 0.6
        else:
            confidence = 0.3

        return {
            "draft_reply": reply,
            "sources": list(set(sources)),
            "confidence": round(confidence, 2)
        }


# Quick test
if __name__ == "__main__":
    resolver = TicketResolver()
    result = resolver.resolve(
        "Customer getting 403 error on API key after plan upgrade"
    )
    print("\n── DRAFT REPLY ──")
    print(result["draft_reply"])
    print("\n── SOURCES ──")
    print(result["sources"])
    print("\n── CONFIDENCE ──")
    print(result["confidence"])
