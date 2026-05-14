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


# api/main.py
# Engineer: E4 Aaditya

import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from agents.ticket_resolver import TicketResolver
from agents.onboarding_bot import OnboardingBot
from agents.churn_advisor import ChurnAdvisor
from api.schemas import (
    TicketRequest, TicketResponse,
    OnboardRequest, OnboardResponse,
    ChurnRequest, ChurnResponse
)

load_dotenv()

app = FastAPI(
    title="NexaSupport RAG API",
    description="AI-powered customer success platform — Groq Cloud + LLaMA 3",
    version="0.1.0"
)

# ── Init agents once at startup ───────────────────────────
print("Initialising agents...")
ticket_resolver = TicketResolver()
churn_advisor = ChurnAdvisor()

# Onboarding bot supports multi-turn sessions
# session_id → OnboardingBot instance
sessions: dict[str, OnboardingBot] = {}

print("All agents ready.")


# ── Health check ──────────────────────────────────────────
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "agents": ["ticket_resolver", "onboarding_bot", "churn_advisor"],
        "vector_db_docs": ticket_resolver.store.count()
    }


# ── UC-1: Ticket Resolver ─────────────────────────────────
@app.post("/ticket", response_model=TicketResponse)
def resolve_ticket(req: TicketRequest):
    try:
        result = ticket_resolver.resolve(
            ticket_text=req.ticket_text,
            top_k=req.top_k
        )
        return TicketResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── UC-2: Onboarding Bot ──────────────────────────────────
@app.post("/onboard", response_model=OnboardResponse)
def onboard_chat(req: OnboardRequest):
    try:
        # get or create session
        if req.session_id not in sessions:
            sessions[req.session_id] = OnboardingBot()

        bot = sessions[req.session_id]
        result = bot.chat(user_message=req.user_message)
        return OnboardResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/onboard/{session_id}")
def reset_session(session_id: str):
    if session_id in sessions:
        sessions[session_id].reset()
        del sessions[session_id]
        return {"status": "session cleared", "session_id": session_id}
    return {"status": "session not found", "session_id": session_id}


# ── UC-3: Churn Advisor ───────────────────────────────────
@app.post("/churn", response_model=ChurnResponse)
def churn_advice(req: ChurnRequest):
    try:
        result = churn_advisor.advise(
            health_profile=req.health_profile,
            top_k=req.top_k
        )
        return ChurnResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))