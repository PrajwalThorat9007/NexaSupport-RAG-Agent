import os
import sys
from dotenv import load_dotenv

load_dotenv()

from ingestion.chunker import load_csv, load_markdown, load_json_profiles
from ingestion.embedder import get_embedder, embed_chunks
from ingestion.vector_store import VectorStore

DATA_DIR = "data"
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")


def ingest_tickets(embedder, store: VectorStore):
    print("\n── UC-1: Ingesting tickets_resolved.csv ──")
    filepath = os.path.join(DATA_DIR, "tickets_resolved.csv")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_csv(filepath)
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def ingest_product_docs(embedder, store: VectorStore):
    print("\n── UC-1 & UC-2: Ingesting product_docs.md ──")
    filepath = os.path.join(DATA_DIR, "product_docs.md")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_markdown(filepath, source_name="product_docs")
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def ingest_onboarding(embedder, store: VectorStore):
    print("\n── UC-2: Ingesting onboarding_guide.md ──")
    filepath = os.path.join(DATA_DIR, "onboarding_guide.md")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_markdown(filepath, source_name="onboarding")
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def ingest_faq(embedder, store: VectorStore):
    print("\n── UC-2: Ingesting faq.md ──")
    filepath = os.path.join(DATA_DIR, "faq.md")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_markdown(filepath, source_name="faq")
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def ingest_churn_playbook(embedder, store: VectorStore):
    print("\n── UC-3: Ingesting churn_playbook.md ──")
    filepath = os.path.join(DATA_DIR, "churn_playbook.md")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_markdown(filepath, source_name="churn_playbook")
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def ingest_customer_health(embedder, store: VectorStore):
    print("\n── UC-3: Ingesting customer_health.json ──")
    filepath = os.path.join(DATA_DIR, "customer_health.json")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} not found")
        return
    chunks = load_json_profiles(filepath)
    print(f"  Chunked into {len(chunks)} pieces")
    chunks = embed_chunks(chunks, embedder)
    store.upsert(chunks)
    print(f"  Done — {store.count()} total docs in store")


def main():
    print("=" * 50)
    print("  NexaSupport — Ingestion Pipeline")
    print("=" * 50)

    # Load shared embedder once
    embedder = get_embedder()

    # One shared ChromaDB collection for all use cases
    store = VectorStore(
        collection_name="nexasupport",
        persist_dir=CHROMA_DIR
    )

    # Run all ingestion functions
    ingest_tickets(embedder, store)
    ingest_product_docs(embedder, store)
    ingest_onboarding(embedder, store)
    ingest_faq(embedder, store)
    ingest_churn_playbook(embedder, store)
    ingest_customer_health(embedder, store)

    print("\n" + "=" * 50)
    print(f"  Ingestion complete!")
    print(f"  Total chunks in ChromaDB: {store.count()}")
    print(f"  Database saved at: {CHROMA_DIR}/")
    print("=" * 50)


if __name__ == "__main__":
    main()