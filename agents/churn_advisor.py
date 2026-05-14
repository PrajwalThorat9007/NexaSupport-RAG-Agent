# churn_advisor.py  —  UC-3
# Responsibility: Given a customer health profile, retrieve similar at-risk
#                 customer histories and generate an intervention plan.
# Owner: Engineer C
#
# TODO: class ChurnAdvisor
#   __init__(self, vector_store: VectorStore, embedder, groq_client)
#     - Store references to shared vector_store, embedder, groq_client
#     - Load prompt template from prompts/churn_advisor.txt
#
#   profile_to_query(self, health_profile: dict) -> str
#     - Convert JSON profile into a natural-language query string
#     - Example: "Customer NPS 3, usage down 65%, renewal in 22 days, billing overdue"
#     - This string is then embedded and used to search the vector store
#
#   advise(self, health_profile: dict, top_k: int = 3) -> dict
#     - Call profile_to_query to get query string
#     - Embed query string
#     - Query vector_store for similar churn playbook chunks + past cases
#     - Build prompt: inject profile + retrieved chunks
#     - Call Groq API
#     - Return: { "intervention_plan": str, "action_items": list[str],
#                 "similar_cases": list[str], "risk_level": str }


# agents/churn_advisor.py — UC-3
# Engineer: E3 Brahmika

import os
from groq import Groq
from dotenv import load_dotenv
from ingestion.embedder import get_embedder, embed_query
from ingestion.vector_store import VectorStore

load_dotenv()


class ChurnAdvisor:
    def __init__(self):
        self.embedder = get_embedder()
        self.store = VectorStore(
            collection_name="nexasupport",
            persist_dir=os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        )
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

        prompt_path = os.path.join("prompts", "churn_advisor.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def profile_to_query(self, health_profile: dict) -> str:
        # Convert JSON profile into a natural language search query
        parts = []

        nps = health_profile.get("nps_score")
        if nps is not None:
            parts.append(f"NPS score {nps}")

        usage_drop = health_profile.get("usage_drop_pct")
        if usage_drop is not None:
            parts.append(f"usage dropped {usage_drop}%")

        days = health_profile.get("days_to_renewal")
        if days is not None:
            parts.append(f"renewal in {days} days")

        status = health_profile.get("health_status")
        if status:
            parts.append(f"account is {status}")

        billing = health_profile.get("billing_events", [])
        if billing:
            parts.append(f"billing issues: {', '.join(billing)}")

        tickets = health_profile.get("open_tickets")
        if tickets:
            parts.append(f"{tickets} open support tickets")

        return "Customer at risk — " + ", ".join(parts)

    def advise(self, health_profile: dict, top_k: int = 3) -> dict:
        # Step 1 — convert profile to query string
        query_text = self.profile_to_query(health_profile)
        print(f"  Query: {query_text}")

        # Step 2 — embed query
        query_embedding = embed_query(query_text, self.embedder)

        # Step 3 — retrieve churn playbook + similar cases
        results = self.store.query(query_embedding, top_k=top_k)
        churn_results = [
            r for r in results
            if any(s in r["source"] for s in ["churn_playbook", "customer_health"])
        ]
        if not churn_results:
            churn_results = results

        # Step 4 — build context
        context_parts = []
        sources = []
        for r in churn_results:
            context_parts.append(r["text"])
            sources.append(r["source"])
        context = "\n\n---\n\n".join(context_parts)

        # Step 5 — build profile string
        profile_str = "\n".join([
            f"Company: {health_profile.get('company_name', 'Unknown')}",
            f"Tier: {health_profile.get('customer_tier', 'Unknown')}",
            f"NPS Score: {health_profile.get('nps_score', 'N/A')}",
            f"Usage Drop: {health_profile.get('usage_drop_pct', 0)}%",
            f"Active Users: {health_profile.get('active_users', 'N/A')} / {health_profile.get('total_seats', 'N/A')} seats",
            f"Days to Renewal: {health_profile.get('days_to_renewal', 'N/A')}",
            f"Last Login: {health_profile.get('last_login_days_ago', 'N/A')} days ago",
            f"Open Tickets: {health_profile.get('open_tickets', 0)}",
            f"Billing Events: {', '.join(health_profile.get('billing_events', [])) or 'None'}",
            f"Health Status: {health_profile.get('health_status', 'Unknown')}",
            f"Notes: {health_profile.get('notes', '')}",
        ])

        # Step 6 — fill prompt
        prompt = self.prompt_template.format(
            profile=profile_str,
            context=context
        )

        # Step 7 — call Groq
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )

        plan = response.choices[0].message.content.strip()

        # Step 8 — determine risk level from profile
        nps = health_profile.get("nps_score", 10)
        usage_drop = health_profile.get("usage_drop_pct", 0)
        days = health_profile.get("days_to_renewal", 365)

        if nps <= 4 and usage_drop >= 50 and days <= 45:
            risk_level = "Critical"
        elif nps <= 6 or usage_drop >= 30 or days <= 90:
            risk_level = "At Risk"
        else:
            risk_level = "Healthy"

        # Step 9 — extract action items from plan text
        action_items = []
        for line in plan.split("\n"):
            line = line.strip()
            if line and line[0].isdigit() and ". " in line:
                action_items.append(line)

        return {
            "intervention_plan": plan,
            "action_items": action_items,
            "similar_cases": list(set(sources)),
            "risk_level": risk_level
        }


# Quick test
if __name__ == "__main__":
    advisor = ChurnAdvisor()

    test_profile = {
        "customer_id": "CUST-007",
        "company_name": "Acme Logistics",
        "customer_tier": "Growth",
        "nps_score": 3,
        "usage_drop_pct": 65,
        "active_users": 4,
        "total_seats": 20,
        "days_to_renewal": 22,
        "last_login_days_ago": 14,
        "open_tickets": 3,
        "billing_events": ["Invoice overdue 14 days", "Failed payment retry x2"],
        "health_status": "Critical",
        "notes": "Champion left the company last month. New point of contact unresponsive."
    }

    result = advisor.advise(test_profile)

    print("\n── INTERVENTION PLAN ──")
    print(result["intervention_plan"])
    print("\n── ACTION ITEMS ──")
    for item in result["action_items"]:
        print(f"  {item}")
    print("\n── SIMILAR CASES ──")
    print(result["similar_cases"])
    print("\n── RISK LEVEL ──")
    print(result["risk_level"])   