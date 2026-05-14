# NexaSupport RAG Agent

> AI-powered customer success platform · Groq Cloud · LLaMA 3 · ChromaDB

## Use Cases
| UC | Agent | Endpoint |
|----|-------|----------|
| UC-1 | Ticket Resolver | `POST /ticket` |
| UC-2 | Onboarding Bot | `POST /onboard` |
| UC-3 | Churn Advisor | `POST /churn` |

## Setup

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. Add dataset files to data/
# (paste generated content into each file under data/)

# 4. Run ingestion (TODO)
python -m ingestion.ingest_all

# 5. Start API
uvicorn api.main:app --reload --port 8000

# 6. (Optional) Start Streamlit UI
streamlit run ui/chat_app.py
```

## Sample curl calls

```bash
# UC-1 Ticket Resolver
curl -X POST http://localhost:8000/ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_text": "Customer getting 403 error on API key after plan upgrade", "top_k": 3}'

# UC-2 Onboarding Bot
curl -X POST http://localhost:8000/onboard \
  -H "Content-Type: application/json" \
  -d '{"user_message": "How do I connect my CRM?", "session_id": "abc123"}'

# UC-3 Churn Advisor
curl -X POST http://localhost:8000/churn \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "CUST-007", "health_profile": {"nps_score": 3, "usage_drop_pct": 65, "days_to_renewal": 20}}'
```

## Tech Stack
- **LLM**: Groq Cloud · llama3-8b-8192
- **Embeddings**: sentence-transformers · all-MiniLM-L6-v2
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **API**: FastAPI + Uvicorn
- **UI**: Streamlit (bonus)

DONE
