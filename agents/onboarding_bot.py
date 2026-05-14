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


class OnboardingBot:
    def __init__(self, vector_store, embedder, groq_client):
        pass

    def chat(self, user_message: str) -> dict:
        pass

    def reset(self) -> None:
        pass
