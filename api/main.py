# main.py
# Responsibility: FastAPI app — wires all 3 agents to HTTP endpoints.
# Owner: Engineer D
#
# TODO: App startup
#   - Load .env (GROQ_API_KEY)
#   - Init shared embedder (get_embedder())
#   - Init shared VectorStore (one collection per UC or one shared collection)
#   - Init Groq client (groq.Groq(api_key=...))
#   - Init TicketResolver, OnboardingBot, ChurnAdvisor with shared deps
#
# TODO: POST /ticket
#   - Accept TicketRequest
#   - Call ticket_resolver.resolve(req.ticket_text, req.top_k)
#   - Return TicketResponse
#
# TODO: POST /onboard
#   - Accept OnboardRequest
#   - Look up or create OnboardingBot session by session_id
#   - Call bot.chat(req.user_message)
#   - Return OnboardResponse
#
# TODO: POST /churn
#   - Accept ChurnRequest
#   - Call churn_advisor.advise(req.health_profile, req.top_k)
#   - Return ChurnResponse
#
# TODO: GET /health
#   - Return { "status": "ok", "collections": { uc1: count, uc2: count, uc3: count } }


from fastapi import FastAPI

app = FastAPI(title="NexaSupport RAG API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/ticket")
def resolve_ticket():
    pass


@app.post("/onboard")
def onboard_chat():
    pass


@app.post("/churn")
def churn_advice():
    pass
