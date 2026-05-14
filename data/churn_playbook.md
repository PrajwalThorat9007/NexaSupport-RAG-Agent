# NexaSupport Customer Success — Churn Risk Playbook

*Internal document — Customer Success Team Operations*
*Last updated: Q4 2024 | Owner: VP Customer Success*

---

## What Is Churn Risk

Churn risk is the probability that a customer will not renew their NexaSupport subscription at the end of their current contract period. Unlike reactive churn — where a customer cancels without warning — the majority of B2B churn is predictable when the right signals are monitored consistently. Our ability to intervene successfully depends on how early we identify at-risk accounts and how quickly we execute the appropriate response.

**Leading indicators** are early warning signs that precede churn by weeks or months. These are the signals we act on proactively:

- A measurable decline in daily active users (DAU) or session frequency over two or more consecutive weeks
- Reduction in API call volume or integration activity relative to the customer's historical baseline
- Decreasing ticket submission rate — paradoxically, customers who stop asking for help are often disengaging, not succeeding
- NPS score dropping below 6 in a pulse survey or CSAT dropping below 70% across recent tickets
- Failure to complete onboarding milestones within 60 days of account creation
- Key stakeholder (admin user) inactivity for 14+ consecutive days
- Unresolved open tickets aging beyond SLA targets without escalation acknowledgment
- Customer initiating conversations about pricing, contract terms, or competitor comparisons
- CRM signals from Salesforce or HubSpot indicating the account is under "budget review" or the champion contact has changed roles

**Lagging indicators** are signals that churn is already highly likely and intervention is urgent:

- Formal downgrade or cancellation request submitted via Billing > Plan & Usage
- Non-payment or repeated payment failures across two or more billing cycles
- Usage drop exceeding 50% within a 30-day window combined with renewal within 60 days
- Executive stakeholder disengaging from scheduled QBRs or Executive Business Reviews without rescheduling
- Public negative reviews on G2, Capterra, or Trustpilot posted by identified customer employees
- Support escalations containing language about "switching providers" or "evaluating alternatives"

Churn risk is not always customer dissatisfaction. Organizational changes, budget cuts, M&A activity, and internal IT consolidation are structural causes that require different intervention strategies than product or service dissatisfaction. CS reps should diagnose root cause before defaulting to discount-based retention responses.

---

## Risk Tier Definitions

NexaSupport classifies customer health into three tiers — Healthy, At Risk, and Critical — based on a composite score derived from usage, NPS, billing status, and renewal proximity. These thresholds are used by both the manual CS review process and the automated customer health monitoring system in the platform.

### Healthy

A customer is classified as Healthy when all of the following conditions are true:
- NPS score is 7 or higher (based on most recent pulse survey within the last 90 days)
- Usage drop over the trailing 30 days is 15% or less relative to the 90-day average
- No open billing events (no failed payments, overdue invoices, or downgrade requests)
- Open ticket count is 2 or fewer
- Admin user last login is within the last 14 days
- No unresolved escalation tickets older than 5 business days

Healthy accounts receive standard success motion: quarterly check-in calls, product update newsletters, feature announcement emails, and renewal touchpoints beginning 90 days before contract end.

### At Risk

A customer is classified as At Risk when one or more of the following thresholds are breached, but the situation has not yet reached Critical severity:
- NPS score is between 5 and 6
- Usage drop is between 16% and 39% over the trailing 30 days
- One active billing event present (e.g., invoice overdue up to 14 days, one failed payment retry)
- Open ticket count is between 3 and 6
- Admin user last login is between 15 and 30 days ago
- Renewal is within 90 days and no renewal conversation has been initiated

At Risk accounts trigger the proactive intervention motion described in Section 4. A CS rep is assigned as the primary owner and must complete an initial outreach within 48 hours of the classification change.

### Critical

A customer is classified as Critical when two or more of the following conditions are simultaneously true, or when any single condition reaches severe threshold:
- NPS score is 4 or lower
- Usage drop exceeds 40% for two or more consecutive weeks AND renewal is within 60 days
- Two or more active billing events present (failed payments, disputes, overdue invoices beyond 14 days)
- Open ticket count exceeds 6 with no resolution trend
- Admin user has not logged in for 30+ days
- Formal downgrade or cancellation request has been submitted
- Renewal is within 30 days with no signed renewal order or active negotiation in progress

Critical accounts require immediate escalation to CS Manager within 4 business hours of classification. Executive sponsor involvement is required for Enterprise Critical accounts. All Critical accounts appear in the weekly CS Leadership churn review meeting.

**Note on manual overrides:** CS reps may manually override health status classifications in the platform under the account's Customer Health panel. All overrides require a written justification and are reviewed weekly by the CS Manager. Do not suppress Critical classifications unless there is confirmed and documented evidence of a recovery path.

---

## Intervention Playbook: Critical Accounts

Critical accounts require immediate, coordinated action from multiple stakeholders. The window for successful intervention is narrow — typically 30 days or less — and every delay reduces recovery probability.

### Step 1: Immediate Internal Triage (Within 4 Business Hours)

1. The CS Manager reviews the account's health dashboard, open tickets, billing events, CRM notes, and recent communication history.
2. Identify the primary churn signal: Is this product dissatisfaction, billing conflict, stakeholder change, or competitive pressure? The intervention strategy differs by root cause.
3. Create a Churn Risk record in Salesforce under the account using the template: Risk Category, Identified Date, Primary Signal, CS Owner, AE Owner, Estimated ARR at Risk, Days to Renewal.
4. Notify the assigned Account Executive (AE) via Slack in the #cs-churn-alerts channel with a brief summary of the account status. AE must acknowledge within 2 hours.
5. If the account is Enterprise tier and ARR exceeds $50,000, escalate to VP Customer Success immediately via the escalation matrix in Section 6.

### Step 2: Executive Business Review (EBR) Scheduling

1. Contact the customer's primary champion via email and phone within 24 hours of triage completion. Use the EBR outreach template from the Talking Points section.
2. Request an executive-level meeting (VP or C-suite) rather than an operational call. Frame the meeting as a strategic alignment session, not a save call.
3. If the champion is unresponsive after two outreach attempts (email + phone within 48 hours), escalate to the AE to leverage their executive relationship. Do not wait more than 72 hours before AE involvement.
4. Schedule the EBR within 7 calendar days of the initial outreach. Meetings scheduled beyond 14 days from identification have significantly lower recovery rates.
5. Prepare the EBR deck using the Critical Account EBR template in Google Drive. Include: usage trend analysis, open ticket summary, roadmap items relevant to the customer's use case, and a proposed success plan with 30/60/90-day milestones.

### Step 3: Root Cause Confirmation

During the EBR or pre-EBR discovery call, confirm the primary churn driver using open-ended questions:
- "Help me understand what's changed on your side since [last positive interaction]."
- "When you imagine your team not using NexaSupport six months from now, what's the most likely reason?"
- "Are there specific outcomes you expected from NexaSupport that haven't been delivered yet?"

Document the confirmed root cause in Salesforce before proceeding with the response strategy. Applying the wrong intervention (e.g., offering a discount when the real issue is a missing feature) damages trust and accelerates churn.

### Step 4: Executive Escalation and Discount Authority

CS Managers can approve one-time discounts up to 15% on renewal ARR without VP approval for At Risk accounts. For Critical accounts, discount authority escalates as follows:
- Up to 20% discount: CS Manager approval
- 21–35% discount: VP Customer Success approval required
- Above 35% or free months: requires sign-off from both VP Customer Success and VP Sales

Discounts should only be offered after root cause is confirmed and the customer has expressed willingness to renew conditionally. Do not lead with pricing concessions before understanding the customer's real objection — leading with discounts signals desperation and often invites further negotiation rather than commitment.

### Step 5: Win-Back Messaging and Success Plan

For accounts where churn is highly probable, deliver a formal Success Plan within 5 business days of the EBR. The plan should include:
- Three specific outcomes NexaSupport will deliver in the next 90 days, tied to the customer's stated goals
- Named internal owner for each outcome (CS rep, product team, or support)
- Escalation contact at VP level with direct phone number
- An optional 30-day extension on current terms to allow the success plan to take effect before the renewal decision is made

Present the Success Plan as a shared Google Doc that both sides co-edit and sign off on. Mutual commitment to the plan significantly increases renewal probability even for deeply at-risk accounts.

---

## Intervention Playbook: At-Risk Accounts

At-Risk accounts represent an earlier stage of potential churn where the right amount of proactive engagement can reverse the trajectory before it becomes critical.

### Proactive Check-In Cadence

At-Risk accounts should receive a structured 30-day engagement sprint from the assigned CS rep:

- **Day 1–3:** Outreach email (use the At-Risk check-in template). Acknowledge any recent support issues by referencing specific ticket IDs. Offer a 30-minute call to review usage and answer questions.
- **Day 7:** Follow-up if no response to the initial email. Use a different channel — Slack, phone, or LinkedIn — to increase response rate.
- **Day 14:** Conduct the check-in call. Use the call to uncover friction, identify unmet use cases, and introduce features the customer may not be using (see Feature Adoption Nudges below).
- **Day 21:** Send a follow-up email summarizing the call, confirming any committed actions from your side, and sharing relevant documentation or training resources.
- **Day 30:** Health status re-evaluation. If usage has recovered and billing issues are resolved, reclassify to Healthy. If the account has deteriorated, immediately reclassify to Critical and execute the Critical playbook.

### Feature Adoption Nudges

At-Risk accounts often show usage drops not because of dissatisfaction but because customers are unaware of features that would solve their current frustrations. Common adoption gaps include:
- Customers on Growth plans who have never configured SLA automations (navigate to Settings > SLA Policies)
- Teams not using routing rules, causing manual triage bottlenecks
- CRM integration configured but bi-directional sync never enabled

During the check-in call, screen-share a demo of one underused feature directly relevant to the customer's industry or role. Keep it to 10 minutes. Do not overwhelm customers with a full feature tour — one relevant demonstration is more effective than an overview of everything.

### Success Plan Templates

For At-Risk accounts, a lighter-weight Success Plan (one-pager rather than a full EBR deck) is appropriate. The one-pager covers: current health status summary, top 2–3 use case gaps, recommended actions (with owner and timeline), and next check-in date. Use the At-Risk Success Plan template from the CS team's shared Google Drive folder under CS Resources > Templates > Success Plans.

---

## Talking Points

### Scenario 1: NPS Score Dropped

*Use when a customer submits an NPS score of 5 or lower and the drop is confirmed over two or more consecutive surveys.*

**Opening:**
> "Hi [Name], I noticed your recent NPS feedback and wanted to reach out personally. I appreciate you sharing that — it's exactly the kind of signal that helps us make sure we're actually delivering value for your team. I'd love to spend 20 minutes understanding what's changed and what we can do better. Do you have time this week for a quick call?"

**Probing:**
> "When you think about what's driving the lower score, is it more about a specific product experience, the level of support you've been getting, or something broader in terms of the value you're seeing from NexaSupport?"

**Closing:**
> "Based on what you've shared, here's what I'm going to personally own over the next 30 days: [specific action 1], [specific action 2]. I'll send you a written summary after this call so we're aligned. Does that sound like a fair starting point?"

---

### Scenario 2: Usage Decline

*Use when usage drops 30% or more and the CS rep needs to initiate a proactive outreach before the customer flags it themselves.*

**Opening:**
> "Hi [Name], I wanted to reach out because our platform data flagged a dip in your team's activity over the last few weeks, and I wanted to check in before assuming everything's fine. Sometimes usage drops are totally benign — your team's been busy, there's a new project, things shift. But I'd rather ask than assume. Are there any blockers or friction points we could help address?"

**Probing:**
> "Are there specific workflows your team was running in NexaSupport that have slowed down or moved to a different tool? I want to understand whether this is a timing thing or whether there's a gap in how we're set up for you."

**Closing:**
> "Would it help to do a brief workflow review together? I can share my screen and walk through the routing and automation setup with you — sometimes small configuration tweaks unlock a lot of value that teams don't realize is available to them."

---

### Scenario 3: Billing Dispute

*Use when a customer has raised a billing complaint, disputed an invoice, or expressed frustration about charges they didn't expect.*

**Opening:**
> "Hi [Name], I saw the note about the invoice discrepancy you raised and I wanted to reach out directly rather than leaving this in the support queue. I completely understand that unexpected charges create friction — let me pull up your account and walk through the invoice line by line so we can resolve this together. I can do that right now if you have a few minutes."

**Probing:**
> "Looking at the invoice, the charge you're questioning appears to be [proration from the plan upgrade / a seat overage / an API usage charge]. Let me explain exactly how that was calculated and then let's confirm whether it matches what you expected based on the change you made on [date]."

**Closing:**
> "I'm going to flag this to our billing team today and ask them to review the charge. If it's a legitimate billing error, we'll issue a credit memo within two business days. If it's accurate but wasn't clearly communicated, I'll ask them to add a detailed line-item explanation to future invoices for your account. Either way, you'll hear from me by [specific date] — is that timeline okay with you?"

---

## Escalation Matrix

When a churn risk account requires involvement beyond the assigned CS rep, use the matrix below to determine who to engage and under what conditions.

| Account ARR | Days to Renewal | Health Status | Required Escalation |
|---|---|---|---|
| Any | ≤ 14 days | Critical | CS Manager + AE (immediate, same business day) |
| < $10,000 | ≤ 30 days | Critical | CS Manager within 4 hours |
| $10,000 – $49,999 | ≤ 45 days | Critical | CS Manager within 4 hours + AE within 24 hours |
| $50,000 – $149,999 | ≤ 60 days | Critical | CS Manager + VP Customer Success within 4 hours |
| ≥ $150,000 | ≤ 90 days | At Risk or Critical | CS Manager + VP Customer Success + VP Sales within 4 hours |
| ≥ $150,000 | ≤ 30 days | Critical | CEO executive sponsor outreach required |

**CS Manager responsibilities in escalation:** Review and approve intervention strategy, authorize discounts within their approval tier, co-own EBR scheduling, participate in the first executive call if the CS rep has not had an executive-level relationship with the account.

**Account Executive responsibilities in escalation:** Leverage existing executive and commercial relationships, co-present the Success Plan during the EBR, lead commercial negotiation if a contract restructuring is required, coordinate with Legal if contract amendments are needed.

**VP Customer Success responsibilities in escalation:** Approve discounts above 20%, participate personally in C-suite calls for accounts over $50,000 ARR, escalate to Product for committed roadmap feature prioritization if the churn signal is feature-gap-related, provide written executive commitment letters for accounts with formal cancellation requests.

**Escalation SLA:** All escalations must be acknowledged in the #cs-churn-alerts Slack channel within the timeframes specified above. Unacknowledged escalations are surfaced in the daily CS leadership standup. CS reps who initiate an escalation are responsible for updating the Salesforce churn risk record within 24 hours of each escalation event.

---

## Success Metrics

Measuring the effectiveness of churn interventions requires tracking both leading recovery indicators and final renewal outcomes. Use the following metrics to evaluate playbook performance on a monthly and quarterly basis.

### Primary Outcome Metrics

- **Renewal Rate:** The percentage of accounts flagged as At Risk or Critical that successfully renew within the target period. Tracked by original risk tier classification. Target: 70% renewal rate for At Risk accounts, 40% for Critical accounts.
- **Churn ARR Recovered:** The dollar value of ARR saved through successful interventions in the measurement period. Calculated as: (Renewed ARR from At Risk and Critical accounts) divided by (Total ARR that was at risk). Report monthly to CS leadership and quarterly to executive team.
- **Downgrade Rate:** The percentage of accounts that renew at a lower ARR than their previous contract. Downgrade is a partial win — the customer stayed but at reduced revenue. Track separately from full churn. Target: downgrades should represent fewer than 20% of intervention outcomes.

### Leading Recovery Indicators

Monitor these signals weekly during an active intervention to assess whether the account is recovering:

- **NPS Recovery:** Has the customer's NPS score increased by 2 or more points in a follow-up survey taken at least 3 weeks after the intervention began? An NPS improvement of 2+ points within 30 days of intervention is the strongest predictor of successful renewal.
- **Usage Lift:** Is weekly active user count trending upward week-over-week for at least 2 consecutive weeks? A usage recovery of 25% or more from the trough level signals a meaningful engagement recovery. Track from the Customer Health dashboard under Analytics > Account Health Trends.
- **Ticket Resolution Rate:** Is the customer's open ticket count declining? A reduction in open tickets combined with positive CSAT scores on resolved tickets indicates that support friction — a common churn driver — is being addressed successfully.
- **Stakeholder Re-engagement:** Has the admin user or executive sponsor logged in within the last 7 days after a period of inactivity? Admin re-engagement is a lagging recovery indicator but confirms that the platform is being actively managed again.
- **Billing Events Cleared:** Have outstanding billing events (overdue invoices, failed payments) been resolved? Billing resolution is necessary but not sufficient for recovery — confirm it is paired with usage and engagement recovery before reclassifying the account.

### Playbook Performance Reviews

The CS team conducts a monthly churn retrospective on the last 90 days of closed churn risk cases. Each retrospective covers:

1. How many accounts were classified At Risk and Critical, broken down by tier and ARR band
2. Intervention completion rate: what percentage of accounts received the full playbook execution vs. partial execution
3. Correlation between intervention speed (time from classification to first outreach) and renewal outcome
4. Playbook gaps: what situations arose that were not covered by current scripts or escalation rules
5. Win-back analysis: for accounts that churned despite intervention, document the primary churn reason and whether an earlier or different intervention could have changed the outcome

Retrospective findings are used to update this playbook quarterly. CS reps are encouraged to submit playbook improvement suggestions via the #cs-ops Slack channel at any time.
