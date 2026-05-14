from agents.churn_advisor import ChurnAdvisor

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

try:
    result = advisor.advise(test_profile)
    print("\n── INTERVENTION PLAN ──")
    print(result["intervention_plan"])
    print("\n── RISK LEVEL ──")
    print(result["risk_level"])
except Exception as e:
    import traceback
    traceback.print_exc()