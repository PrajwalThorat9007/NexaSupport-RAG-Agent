# onboarding_bot.py  —  UC-2
# Responsibility: Multi-turn conversational RAG agent for onboarding Q&A.
#                 Grounds answers in onboarding_guide.md and faq.md.
# Owner: Engineer B
#
# TODO: class OnboardingBot
#   __init__(self, vector_store: VectorStore, embedder, groq_client)
#     - Store references to shared vector_store, embedder, groq_client
#     - Load prompt template from prompts/onboarding_bot.txt
#     - Init self.history = []  (list of {"role": str, "content": str})
#
#   chat(self, user_message: str) -> dict
#     - Embed user_message
#     - Query vector_store top_k=3 (filter source in ["onboarding", "faq"])
#     - Build prompt with: system instructions + retrieved context + chat history + user_message
#     - Call Groq API
#     - Append user + assistant turns to self.history
#     - Return: { "answer": str, "sources": list[str], "history_length": int }
#
#   reset(self) -> None
#     - Clear self.history


# agents/onboarding_bot.py — UC-2
# Engineer: E2 Barnam

import os
from groq import Groq
from dotenv import load_dotenv
from ingestion.embedder import get_embedder, embed_query
from ingestion.vector_store import VectorStore

load_dotenv()


class OnboardingBot:
    def __init__(self):
        self.embedder = get_embedder()
        self.store = VectorStore(
            collection_name="nexasupport",
            persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        )
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        self.history = []

        prompt_path = os.path.join("prompts", "onboarding_bot.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def chat(self, user_message: str, top_k: int = 3) -> dict:
        # Step 1 — embed user message
        query_embedding = embed_query(user_message, self.embedder)

        # Step 2 — retrieve relevant chunks
        # filter to onboarding, faq, product_docs sources only
        results = self.store.query(query_embedding, top_k=top_k)
        onboarding_results = [
            r for r in results
            if any(s in r["source"] for s in ["onboarding", "faq", "product_docs"])
        ]
        # fallback to all results if filter returns nothing
        if not onboarding_results:
            onboarding_results = results

        # Step 3 — build context
        context_parts = []
        sources = []
        for r in onboarding_results:
            context_parts.append(r["text"])
            sources.append(r["source"])
        context = "\n\n---\n\n".join(context_parts)

        # Step 4 — build history string
        history_str = ""
        for turn in self.history:
            history_str += f"Customer: {turn['user']}\nAssistant: {turn['assistant']}\n\n"

        # Step 5 — fill prompt
        prompt = self.prompt_template.format(
            history=history_str if history_str else "No previous conversation.",
            context=context,
            user_message=user_message
        )

        # Step 6 — call Groq
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )

        answer = response.choices[0].message.content.strip()

        # Step 7 — save to history
        self.history.append({
            "user": user_message,
            "assistant": answer
        })

        return {
            "answer": answer,
            "sources": list(set(sources)),
            "history_length": len(self.history)
        }

    def reset(self):
        self.history = []
        print("Conversation history cleared.")


# Quick test — multi turn
if __name__ == "__main__":
    bot = OnboardingBot()

    # Turn 1
    print("\n── TURN 1 ──")
    q1 = "How do I connect my CRM to NexaSupport and set up auto-tagging?"
    print(f"Customer: {q1}")
    r1 = bot.chat(q1)
    print(f"Bot: {r1['answer']}")
    print(f"Sources: {r1['sources']}")
    print(f"History length: {r1['history_length']}")

    # Turn 2 — follow up
    print("\n── TURN 2 ──")
    q2 = "What if the CRM sync fails after I connect it?"
    print(f"Customer: {q2}")
    r2 = bot.chat(q2)
    print(f"Bot: {r2['answer']}")
    print(f"Sources: {r2['sources']}")
    print(f"History length: {r2['history_length']}")
