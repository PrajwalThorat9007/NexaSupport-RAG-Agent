# NexaSupport RAG Agent

> An AI-powered customer success platform built with Retrieval-Augmented Generation (RAG), Groq Cloud, LLaMA 3, and ChromaDB. Three specialized agents handle ticket resolution, customer onboarding Q&A, and churn risk intervention — all grounded in a shared vector knowledge base.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Use Cases](#use-cases)
  - [UC-1: Ticket Resolver](#uc-1-ticket-resolver)
  - [UC-2: Onboarding Bot](#uc-2-onboarding-bot)
  - [UC-3: Churn Advisor](#uc-3-churn-advisor)
- [RAG Pipeline — How It Works](#rag-pipeline--how-it-works)
- [Knowledge Base](#knowledge-base)
- [API Reference](#api-reference)
- [Streamlit UI](#streamlit-ui)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Design Decisions](#design-decisions)
- [Interview Q&A Prep](#interview-qa-prep)

---

## Project Overview

NexaSupport RAG Agent is a multi-agent AI system designed for B2B customer success teams. Instead of a single general-purpose chatbot, the system uses **three purpose-built agents**, each with its own prompt, retrieval strategy, and output schema — all sharing one ChromaDB vector store.

**The core problem it solves:**
- Support agents waste time drafting replies to tickets that have been solved before
- New customers get lost during onboarding and can't find answers in documentation
- Customer success teams miss churn signals until it's too late to intervene

**How it solves them:**
- Embeds all historical tickets, product docs, onboarding guides, FAQs, churn playbooks, and customer health profiles into a vector database
- At query time, retrieves the most semantically relevant chunks and injects them into a structured LLM prompt
- Returns structured, actionable outputs — not just raw text


---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│         FastAPI REST API  ·  Streamlit Chat UI                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        AGENT LAYER                              │
│                                                                 │
│   ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│   │  TicketResolver │  │  OnboardingBot   │  │ ChurnAdvisor │  │
│   │    (UC-1)       │  │    (UC-2)        │  │   (UC-3)     │  │
│   │                 │  │  multi-turn      │  │              │  │
│   │ ticket → draft  │  │  session memory  │  │ profile →    │  │
│   │ reply + conf.   │  │  + sources       │  │ action plan  │  │
│   └────────┬────────┘  └────────┬─────────┘  └──────┬───────┘  │
└────────────┼────────────────────┼────────────────────┼──────────┘
             │                    │                    │
┌────────────▼────────────────────▼────────────────────▼──────────┐
│                      RAG PIPELINE                               │
│                                                                 │
│   Query Text → Embedder (all-MiniLM-L6-v2)                      │
│              → ChromaDB cosine similarity search                │
│              → Top-K chunks retrieved                           │
│              → Prompt template filled                           │
│              → Groq API (LLaMA 3.3 70B)                         │
│              → Structured response returned                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    VECTOR STORE (ChromaDB)                      │
│                                                                 │
│  tickets_resolved.csv  ·  product_docs.md  ·  onboarding_guide  │
│  faq.md  ·  churn_playbook.md  ·  customer_health.json          │
└─────────────────────────────────────────────────────────────────┘
```


---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| LLM Inference | [Groq Cloud](https://groq.com) + LLaMA 3.3 70B | Ultra-fast inference (~500 tokens/sec), free tier available |
| Embeddings | `sentence-transformers` — `all-MiniLM-L6-v2` | Local, no API cost, 384-dim vectors, strong semantic quality |
| Vector Store | [ChromaDB](https://www.trychroma.com) (persistent) | Embedded, no server needed, cosine similarity, easy upsert |
| API Framework | FastAPI + Uvicorn | Async, auto-docs via Swagger, Pydantic validation |
| UI | Streamlit | Rapid chat UI with session state, no frontend code needed |
| Data Handling | Pandas, LangChain `RecursiveCharacterTextSplitter` | CSV ingestion + smart text chunking with overlap |
| Config | `python-dotenv` | Secrets management via `.env` |
| Testing | Pytest | Smoke tests for all three agents |

---

## Project Structure

```
NexaSupport-RAG-Agent/
│
├── agents/                     # The three AI agents
│   ├── ticket_resolver.py      # UC-1: Draft reply for support tickets
│   ├── onboarding_bot.py       # UC-2: Multi-turn onboarding Q&A
│   ├── churn_advisor.py        # UC-3: Churn risk intervention planner
│   └── __init__.py
│
├── api/                        # FastAPI REST layer
│   ├── main.py                 # Route definitions, agent wiring
│   ├── schemas.py              # Pydantic request/response models
│   └── __init__.py
│
├── ingestion/                  # RAG data pipeline
│   ├── chunker.py              # Text splitting, CSV/MD/JSON loaders
│   ├── embedder.py             # Sentence-transformer embedding
│   ├── vector_store.py         # ChromaDB upsert + query wrapper
│   └── __init__.py
│
├── prompts/                    # LLM prompt templates (plain text)
│   ├── ticket_resolver.txt
│   ├── onboarding_bot.txt
│   └── churn_advisor.txt
│
├── data/                       # Knowledge base source files
│   ├── tickets_resolved.csv    # Historical resolved support tickets
│   ├── product_docs.md         # Full product documentation
│   ├── onboarding_guide.md     # Step-by-step onboarding guide
│   ├── faq.md                  # Frequently asked questions
│   ├── churn_playbook.md       # CS team churn intervention playbook
│   └── customer_health.json    # Customer health profiles (NPS, usage, etc.)
│
├── ui/
│   └── chat_app.py             # Streamlit chat UI for OnboardingBot
│
├── tests/
│   └── test_all_agents.py      # Pytest smoke tests for all 3 agents
│
├── ingest_all.py               # One-shot ingestion script (run once)
├── test_groq.py                # Quick Groq API connectivity test
├── test_churn.py               # Standalone churn advisor test
├── requirements.txt
├── .env.example
└── README.md
```


---

## Use Cases

### UC-1: Ticket Resolver

**Problem:** Support agents spend time writing replies to tickets that are nearly identical to ones already resolved. Institutional knowledge lives in spreadsheets and is never reused.

**Solution:** Given a new ticket description, the agent embeds it, retrieves the top-3 most similar past resolutions from ChromaDB, injects them into a structured prompt, and returns a ready-to-send draft reply with a confidence score.

**Confidence Score Logic:**
- Average cosine distance < 0.3 → `1.0` (High — very similar past tickets found)
- Average cosine distance < 0.6 → `0.6` (Medium)
- Average cosine distance ≥ 0.6 → `0.3` (Low — escalate to Tier 2)

**Input:**
```json
{
  "ticket_text": "Customer getting 403 error on API key after plan upgrade",
  "top_k": 3
}
```

**Output:**
```json
{
  "draft_reply": "Hi [Customer], after a plan upgrade your existing API key...",
  "sources": ["tickets:TKT-0042", "faq:Why is my API key returning a 403 error"],
  "confidence": 1.0
}
```

---

### UC-2: Onboarding Bot

**Problem:** New customers ask the same onboarding questions repeatedly. Support agents answer them manually, and the answers are inconsistent.

**Solution:** A multi-turn conversational RAG agent grounded in `onboarding_guide.md`, `faq.md`, and `product_docs.md`. It maintains per-session conversation history so follow-up questions are answered in context.

**Key Design Choices:**
- Session state is stored in-memory as a dict keyed by `session_id` (UUID)
- Each turn appends to `self.history` — the full history is injected into every subsequent prompt
- Source filtering ensures only onboarding/FAQ/product_docs chunks are retrieved (not churn data)
- Fallback: if filtered results are empty, it falls back to all results

**Input:**
```json
{
  "user_message": "What if the CRM sync fails after I connect it?",
  "session_id": "abc-123"
}
```

**Output:**
```json
{
  "answer": "If your CRM sync fails, navigate to Integrations > Marketplace...",
  "sources": ["onboarding:Connect Your CRM", "faq:Salesforce sync not updating"],
  "history_length": 2
}
```


---

### UC-3: Churn Advisor

**Problem:** Customer success teams often miss churn signals until renewal is days away. When they do act, they don't know what intervention to apply or what to say.

**Solution:** Given a customer health profile (NPS score, usage drop %, days to renewal, billing events, open tickets), the agent converts it to a natural-language query, retrieves relevant churn playbook sections and similar past cases, and generates a structured intervention plan with action items, talking points, and escalation guidance.

**Risk Classification Logic (rule-based, applied after LLM response):**
- `Critical`: NPS ≤ 4 AND usage drop ≥ 50% AND days to renewal ≤ 45
- `At Risk`: NPS ≤ 6 OR usage drop ≥ 30% OR days to renewal ≤ 90
- `Healthy`: everything else

**Input:**
```json
{
  "customer_id": "CUST-007",
  "health_profile": {
    "company_name": "Acme Logistics",
    "customer_tier": "Growth",
    "nps_score": 3,
    "usage_drop_pct": 65,
    "active_users": 4,
    "total_seats": 20,
    "days_to_renewal": 22,
    "open_tickets": 3,
    "billing_events": ["Invoice overdue 14 days", "Failed payment retry x2"],
    "health_status": "Critical",
    "notes": "Champion left the company last month."
  },
  "top_k": 3
}
```

**Output:**
```json
{
  "intervention_plan": "Risk Level: Critical\n\nSituation Summary: ...",
  "action_items": [
    "1. Schedule EBR with new point of contact within 48 hours — CS Manager",
    "2. Resolve overdue invoice — Billing team by EOD",
    ...
  ],
  "similar_cases": ["churn_playbook:Critical Accounts", "customer_health:CUST-003"],
  "risk_level": "Critical"
}
```

---

## RAG Pipeline — How It Works

Understanding the RAG pipeline end-to-end is critical for interviews. Here's exactly what happens at each stage.

### Stage 1: Ingestion (run once with `ingest_all.py`)

```
Raw Data Files
     │
     ▼
chunker.py
  ├── load_csv()         → reads tickets_resolved.csv, combines issue + resolution per row
  ├── load_markdown()    → splits .md files by ## headings, then chunks each section
  └── load_json_profiles() → converts customer health JSON into descriptive text blocks
     │
     ▼ list of {"text", "source", "chunk_index"}
     │
embedder.py
  └── embed_chunks()     → batch encodes all chunks using all-MiniLM-L6-v2 (384-dim)
     │
     ▼ chunks now have "embedding" key added
     │
vector_store.py
  └── upsert()           → stores in ChromaDB with cosine similarity index
                           ID format: "{source}__chunk{index}"
```

**Chunking strategy:**
- `RecursiveCharacterTextSplitter` with `chunk_size=500`, `overlap=50`
- Separators: `["\n\n", "\n", ".", " "]` — tries paragraph breaks first, then sentences
- Overlap ensures context isn't lost at chunk boundaries

**Why `all-MiniLM-L6-v2`?**
- 384-dimensional vectors — small and fast
- Trained on semantic similarity tasks — great for Q&A retrieval
- Runs locally — zero API cost for embeddings
- Singleton pattern in `get_embedder()` — model loaded once, reused across all agents

### Stage 2: Query Time (every agent call)

```
User Input (ticket text / question / health profile)
     │
     ▼
embed_query()            → single vector (384-dim float list)
     │
     ▼
VectorStore.query()      → ChromaDB cosine similarity search, returns top-K
                           each result: {"text", "source", "distance"}
     │
     ▼
Source filtering         → each agent filters results to its relevant sources
                           (e.g., OnboardingBot only uses onboarding/faq/product_docs)
     │
     ▼
Prompt template fill     → context chunks + user input injected into .txt template
     │
     ▼
Groq API call            → LLaMA 3.3 70B, temperature=0.3, max_tokens=1024
     │
     ▼
Structured response      → parsed and returned as typed dict
```


---

## Knowledge Base

The vector store is populated from six source files, each serving a different agent:

| File | Type | Used By | Content |
|---|---|---|---|
| `tickets_resolved.csv` | CSV | UC-1 | Historical support tickets with issue descriptions, product area, tags, and resolutions |
| `product_docs.md` | Markdown | UC-1, UC-2 | Full product documentation — API auth, webhooks, billing, integrations, SLA, roles |
| `onboarding_guide.md` | Markdown | UC-2 | 6-step onboarding guide covering account setup, CRM connection, routing rules, automations |
| `faq.md` | Markdown | UC-2 | 10 detailed FAQs covering 403 errors, API key rotation, rate limits, billing disputes, CRM sync |
| `churn_playbook.md` | Markdown | UC-3 | Internal CS playbook — risk tier definitions, intervention steps, talking points, escalation matrix |
| `customer_health.json` | JSON | UC-3 | Customer health profiles with NPS, usage drop %, renewal dates, billing events, open tickets |

**Source naming convention in ChromaDB:**
- `tickets:TKT-0042` — from CSV, ticket ID as suffix
- `onboarding:Connect Your CRM` — from markdown, section heading as suffix
- `faq:Why is my API key returning a 403 error` — from FAQ markdown
- `churn_playbook:Critical Accounts` — from churn playbook section
- `customer_health:CUST-007` — from JSON profile, customer ID as suffix
- `product_docs:API Authentication` — from product docs section

This naming convention lets each agent filter retrieved results to only its relevant sources.

---

## API Reference

The FastAPI server exposes four endpoints. Auto-generated Swagger docs are available at `http://localhost:8000/docs` when the server is running.

### `GET /health`
Returns server status and total document count in ChromaDB.

```json
{
  "status": "ok",
  "agents": ["ticket_resolver", "onboarding_bot", "churn_advisor"],
  "vector_db_docs": 342
}
```

### `POST /ticket`
Resolves a support ticket by retrieving similar past resolutions and generating a draft reply.

**Request:**
```json
{ "ticket_text": "string", "top_k": 3 }
```
**Response:**
```json
{ "draft_reply": "string", "sources": ["string"], "confidence": 0.0 }
```

### `POST /onboard`
Multi-turn onboarding Q&A. Pass the same `session_id` across turns to maintain conversation history.

**Request:**
```json
{ "user_message": "string", "session_id": "string" }
```
**Response:**
```json
{ "answer": "string", "sources": ["string"], "history_length": 0 }
```

### `DELETE /onboard/{session_id}`
Clears conversation history for a given session.

### `POST /churn`
Generates a churn intervention plan from a customer health profile.

**Request:**
```json
{
  "customer_id": "string",
  "health_profile": { "nps_score": 3, "usage_drop_pct": 65, ... },
  "top_k": 3
}
```
**Response:**
```json
{
  "intervention_plan": "string",
  "action_items": ["string"],
  "similar_cases": ["string"],
  "risk_level": "Critical | At Risk | Healthy"
}
```


---

## Streamlit UI

A browser-based chat interface for the Onboarding Bot (UC-2) is available in `ui/chat_app.py`.

**Features:**
- Full chat history rendered with `st.chat_message`
- Source attribution shown below each assistant response
- Sidebar with example questions (clickable) and session reset button
- Session ID displayed for debugging
- Directly instantiates `OnboardingBot` — no HTTP call needed

**Run it:**
```bash
streamlit run ui/chat_app.py
```

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- A free [Groq Cloud](https://console.groq.com) account and API key

### 1. Clone the repository
```bash
git clone https://github.com/your-username/NexaSupport-RAG-Agent.git
cd NexaSupport-RAG-Agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=llama-3.3-70b-versatile
TOP_K=3
```

### 5. Run the ingestion pipeline (one-time setup)
This loads all data files, embeds them, and saves to ChromaDB:
```bash
python ingest_all.py
```
Expected output:
```
Loading embedding model (first time only)...
── UC-1: Ingesting tickets_resolved.csv ──
── UC-1 & UC-2: Ingesting product_docs.md ──
── UC-2: Ingesting onboarding_guide.md ──
── UC-2: Ingesting faq.md ──
── UC-3: Ingesting churn_playbook.md ──
── UC-3: Ingesting customer_health.json ──
Ingestion complete! Total chunks in ChromaDB: ~300+
```

---

## Running the Project

### Start the FastAPI server
```bash
uvicorn api.main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Start the Streamlit UI
```bash
streamlit run ui/chat_app.py
```

### Run individual agent tests
```bash
python agents/ticket_resolver.py
python agents/onboarding_bot.py
python agents/churn_advisor.py
```

### Verify Groq connectivity
```bash
python test_groq.py
```

### Run the test suite
```bash
pytest tests/
```


---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Your Groq Cloud API key | Required |
| `CHROMA_PERSIST_DIR` | Path where ChromaDB stores its data | `./chroma_db` |
| `EMBEDDING_MODEL` | Sentence-transformer model name | `all-MiniLM-L6-v2` |
| `LLM_MODEL` | Groq model ID | `llama-3.3-70b-versatile` |
| `TOP_K` | Default number of chunks to retrieve | `3` |

---

## Design Decisions

These are the choices worth explaining in an interview — each one has a reason.

**One shared ChromaDB collection for all agents**
All six data sources are stored in a single `nexasupport` collection. Each agent filters retrieved results by source prefix at query time. This avoids managing multiple collections while still giving each agent domain-specific context. The tradeoff is that a very large knowledge base could return irrelevant cross-domain results — mitigated by the source filtering logic in each agent.

**Local embeddings, cloud LLM**
`all-MiniLM-L6-v2` runs locally — no API cost, no latency for embedding. The LLM call (Groq) is where the reasoning happens, so that's where the cloud API is used. This keeps costs near zero during development.

**Temperature = 0.3**
Low temperature makes the LLM more deterministic and factual. For support use cases, consistency matters more than creativity. The model should follow the retrieved context closely, not hallucinate.

**Singleton embedder pattern**
`get_embedder()` uses a module-level `_embedder` variable. The 80MB model is loaded once per process and reused across all agents and all requests. Without this, every API call would reload the model from disk.

**Prompt templates as `.txt` files**
Prompts are stored outside Python code so they can be edited without touching agent logic. Each template uses `{placeholder}` format strings filled at runtime. This separation makes prompt iteration fast.

**Session management for OnboardingBot**
The API layer maintains a `sessions: dict[str, OnboardingBot]` dictionary. Each `session_id` maps to its own bot instance with its own `self.history`. This gives true multi-turn memory without a database. The tradeoff is that sessions are lost on server restart — acceptable for a demo/prototype.

**Confidence score from cosine distance**
Rather than asking the LLM to self-assess confidence (which is unreliable), the confidence score is derived from the average cosine distance of retrieved chunks. Low distance = high similarity = high confidence. This is a more objective signal.

**Rule-based risk classification in ChurnAdvisor**
The `risk_level` field is computed from hard thresholds on NPS, usage drop, and days to renewal — not from the LLM output. This makes the classification auditable and consistent. The LLM generates the narrative plan; the code generates the classification.


---

## Interview Q&A Prep

These are the questions a reviewer is most likely to ask. Read these before your interview.

---

**Q: What is RAG and why did you use it instead of fine-tuning?**

RAG (Retrieval-Augmented Generation) retrieves relevant documents at query time and injects them into the LLM prompt as context. Fine-tuning bakes knowledge into model weights. RAG is better here because: (1) the knowledge base can be updated without retraining, (2) it's transparent — you can see exactly which chunks were retrieved, (3) it's far cheaper — no GPU training required, and (4) it handles factual, domain-specific Q&A better than a fine-tuned general model.

---

**Q: How does ChromaDB work and why did you choose it?**

ChromaDB is an embedded vector database. It stores vectors alongside their metadata and supports approximate nearest-neighbor search using HNSW (Hierarchical Navigable Small World) graphs with cosine similarity. It was chosen because it runs in-process (no separate server), persists to disk, and has a simple Python API. For production at scale, you'd consider Pinecone, Weaviate, or pgvector.

---

**Q: What is cosine similarity and why is it used for vector search?**

Cosine similarity measures the angle between two vectors, not their magnitude. Two texts with similar meaning will have embeddings that point in similar directions, regardless of length. ChromaDB returns cosine distance (1 - cosine similarity), so lower distance = more similar. This is why a distance < 0.3 maps to high confidence in the TicketResolver.

---

**Q: Why `all-MiniLM-L6-v2` specifically?**

It's a distilled model trained on semantic similarity tasks — it maps sentences with similar meaning to nearby points in 384-dimensional space. It's fast (runs on CPU), small (~80MB), and performs well on retrieval benchmarks. The 384-dim vectors are compact enough for fast search even with thousands of chunks.

---

**Q: How does the OnboardingBot maintain conversation context?**

Each `OnboardingBot` instance has a `self.history` list. Every `chat()` call appends the user message and assistant response as a dict. On the next call, the full history is serialized to a string and injected into the prompt template under `{history}`. The LLM sees the entire conversation and can answer follow-up questions in context. The session is identified by a UUID passed in every API request.

---

**Q: What happens if the vector store returns irrelevant results?**

Each agent has a source filter — for example, `OnboardingBot` only uses chunks from `onboarding`, `faq`, and `product_docs` sources. If the filter returns nothing (e.g., the question is completely out of domain), it falls back to all results. The prompt template also instructs the LLM: "If the context does not contain the answer, say: I don't have that info — please contact support." This prevents hallucination.

---

**Q: How would you scale this to production?**

Several changes would be needed: (1) Replace in-memory session storage with Redis or a database, (2) Replace ChromaDB with a managed vector DB like Pinecone or Weaviate, (3) Add authentication to the FastAPI endpoints, (4) Add async LLM calls using `asyncio` to handle concurrent requests, (5) Add a proper logging layer (structured logs, request IDs), (6) Containerize with Docker and deploy behind a load balancer, (7) Add a re-ranking step (cross-encoder) after initial retrieval for better precision.

---

**Q: Why is temperature set to 0.3?**

Temperature controls randomness in LLM output. At 0.0, the model always picks the highest-probability token (fully deterministic). At 1.0, it samples more freely. 0.3 is a low-temperature setting that keeps the model focused and factual — important for support use cases where consistency and accuracy matter more than creativity. Higher temperature would risk the model drifting from the retrieved context.

---

**Q: What is the chunking strategy and why does overlap matter?**

Text is split using `RecursiveCharacterTextSplitter` with `chunk_size=500` characters and `overlap=50`. The splitter tries to break at paragraph boundaries first (`\n\n`), then line breaks, then sentences, then spaces. Overlap means the last 50 characters of one chunk are repeated at the start of the next. This prevents a sentence that spans a chunk boundary from losing its context — without overlap, a key phrase split across two chunks might not be retrieved by either.

---

**Q: How does the ChurnAdvisor convert a JSON profile to a search query?**

The `profile_to_query()` method extracts key fields (NPS score, usage drop %, days to renewal, health status, billing events, open tickets) and assembles them into a natural-language sentence like: `"Customer at risk — NPS score 3, usage dropped 65%, renewal in 22 days, account is Critical, billing issues: Invoice overdue 14 days"`. This sentence is then embedded and used to search the vector store for similar churn playbook sections and past customer cases.

---

**Q: What would you improve if you had more time?**

1. Implement a re-ranking step using a cross-encoder model to improve retrieval precision
2. Add streaming responses from Groq for better UX in the Streamlit UI
3. Implement proper session persistence (Redis) so sessions survive server restarts
4. Add evaluation metrics — measure retrieval recall and answer faithfulness using RAGAS
5. Complete the test suite with real assertions (currently the tests are stubs)
6. Add a feedback loop — let agents learn from thumbs up/down on responses
7. Implement hybrid search (keyword + semantic) for better recall on exact-match queries

---

*Built as part of BridgeLabz AI/ML training program.*
