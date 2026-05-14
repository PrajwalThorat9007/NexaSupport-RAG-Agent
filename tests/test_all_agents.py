# test_all_agents.py
# Responsibility: End-to-end smoke tests for all 3 use cases.
# Owner: Engineer D
#
# TODO: test_ticket_resolver()
#   - Input: "Customer getting 403 error on API key after plan upgrade"
#   - Assert: response has "draft_reply", "sources" (non-empty), "confidence" (0–1)
#
# TODO: test_onboarding_bot_single_turn()
#   - Input: "How do I connect my CRM to NexaSupport?"
#   - Assert: response has "answer", "sources" contains "onboarding" or "faq"
#
# TODO: test_onboarding_bot_multi_turn()
#   - Turn 1: "How do I set up auto-tagging?"
#   - Turn 2: "What if the CRM sync fails?"
#   - Assert: history_length == 2 after turn 2
#
# TODO: test_churn_advisor()
#   - Input: { nps_score: 3, usage_drop_pct: 65, days_to_renewal: 20, ... }
#   - Assert: response has "intervention_plan", "action_items" (list len >= 3)
#   - Assert: risk_level == "Critical"
#
# Run with:  pytest tests/


import pytest


def test_ticket_resolver():
    pass


def test_onboarding_bot_single_turn():
    pass


def test_onboarding_bot_multi_turn():
    pass


def test_churn_advisor():
    pass
