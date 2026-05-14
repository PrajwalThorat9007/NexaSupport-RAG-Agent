# schemas.py
# Responsibility: Pydantic request and response models for all 3 endpoints.
# Owner: Engineer D
#
# TODO: class TicketRequest(BaseModel)
#   - ticket_text: str
#   - top_k: int = 3
#
# TODO: class TicketResponse(BaseModel)
#   - draft_reply: str
#   - sources: list[str]
#   - confidence: float
#
# TODO: class OnboardRequest(BaseModel)
#   - user_message: str
#   - session_id: str  # used to look up conversation history
#
# TODO: class OnboardResponse(BaseModel)
#   - answer: str
#   - sources: list[str]
#   - history_length: int
#
# TODO: class ChurnRequest(BaseModel)
#   - customer_id: str
#   - health_profile: dict  # raw JSON from customer_health.json
#   - top_k: int = 3
#
# TODO: class ChurnResponse(BaseModel)
#   - intervention_plan: str
#   - action_items: list[str]
#   - similar_cases: list[str]
#   - risk_level: str


# api/schemas.py
# Engineer: E4 Aaditya

from pydantic import BaseModel


# ── UC-1 Ticket Resolver ──────────────────────────────────
class TicketRequest(BaseModel):
    ticket_text: str
    top_k: int = 3


class TicketResponse(BaseModel):
    draft_reply: str
    sources: list[str]
    confidence: float


# ── UC-2 Onboarding Bot ───────────────────────────────────
class OnboardRequest(BaseModel):
    user_message: str
    session_id: str


class OnboardResponse(BaseModel):
    answer: str
    sources: list[str]
    history_length: int


# ── UC-3 Churn Advisor ────────────────────────────────────
class ChurnRequest(BaseModel):
    customer_id: str
    health_profile: dict
    top_k: int = 3


class ChurnResponse(BaseModel):
    intervention_plan: str
    action_items: list[str]
    similar_cases: list[str]
    risk_level: str