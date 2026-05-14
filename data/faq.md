# NexaSupport — Frequently Asked Questions

---

## Why is my API key returning a 403 error after I upgraded my plan?

A 403 Forbidden response after a plan upgrade almost always means the API key you are using was scoped to your previous workspace or plan tier and has not been updated to reflect the new permissions. When a plan upgrade occurs, NexaSupport may provision a new workspace context or expand permission scopes that existing keys do not automatically inherit.

To resolve this, navigate to Settings > Developer > API Keys and review the key currently in use. Check the Workspace column — if it shows a legacy or inactive workspace name, that key will not work against the new plan's endpoints. Generate a new key by clicking Create New Key, select the appropriate permission scopes for your use case (e.g., tickets.read, tickets.write, analytics.export), and copy the key immediately as it will only be shown once.

Update the X-API-KEY header in your application or environment variables with the new key value and retry the failing request. Also verify that the API endpoint URL uses your correct workspace subdomain (e.g., yourcompany.nexasupport.com/v1/). If requests were previously working against a sandbox environment, confirm you are now pointing to the production base URL.

If the 403 persists after replacing the key, open the API Audit Log under Settings > Developer > Audit Log and look for the specific failed request. The audit entry will include a rejection_reason field that can identify whether the issue is a scope mismatch, IP restriction, or workspace suspension.

**Tip:** After any plan upgrade, audit all active API keys from the Key Management panel and re-scope them to take advantage of new permission levels unlocked by your new plan tier.

---

## How do I rotate my API key without causing downtime?

API key rotation is a routine security practice and NexaSupport supports zero-downtime rotation through a brief overlap window between old and new credentials.

Start by generating a replacement key: go to Settings > Developer > API Keys and click Create New Key. Assign the same permission scopes as the key being replaced. Copy the new key value and store it securely in your secrets manager or environment variable store. Do not revoke the old key yet.

Next, update your application's configuration to use the new key. Deploy the change to one service or environment at a time rather than all at once, especially in production. Once the new key is confirmed working — you can verify this by checking the API Audit Log for successful 200 responses tied to the new key's identifier — proceed to revoke the old key by clicking the Revoke button next to it in the Key Management panel.

Enterprise workspaces with mandatory key expiration policies (configurable under Settings > Security > Key Expiration) will receive a warning notification 14 days before a key expires. This gives your team time to complete rotation before authentication failures begin. If a key expires before rotation is complete, re-generate a new key and treat it as an emergency rotation.

The rotation process typically takes less than 10 minutes end-to-end if your deployment pipeline is ready. Avoid rotating keys during peak traffic periods unless a security incident requires immediate revocation.

**Note:** NexaSupport does not support automatic key rotation — all key lifecycle events require deliberate admin action. Schedule rotations as recurring tasks in your operations calendar every 90 days at minimum.

---

## Why am I receiving a 429 Too Many Requests error and how do I handle it?

A 429 response means your application has exceeded the rate limit assigned to your API key's plan tier. NexaSupport enforces the following rate limits: Starter plans are capped at 60 requests per minute, Growth plans at 300 requests per minute, and Enterprise plans receive custom rate allocations negotiated at contract time.

The most common cause of unexpected 429 errors is running parallel API workers that share a single API key, effectively multiplying the request rate beyond the per-key limit. Background jobs, data export scripts, and webhook-triggered workflows are frequent culprits when they run concurrently without rate awareness.

To handle 429 responses correctly, your API client should read the Retry-After response header, which specifies how many seconds to wait before retrying. Additionally, monitor the X-RateLimit-Remaining header in each response to track your remaining quota within the current window. Implement exponential backoff in your retry logic so that repeated failures do not generate a burst of retries that further exhaust your quota.

If your legitimate workload consistently approaches or exceeds your plan limit, navigate to Settings > Developer > Usage Metrics to review your request volume trends over the past 30 days. If you are on a Starter or Growth plan and regularly hitting limits, consider upgrading your plan or contacting your account manager to discuss a rate limit increase.

For bulk data operations such as large ticket exports or historical data processing, use the Export API endpoints (/v1/exports/tickets) which are optimized for high-volume extraction and operate under separate, more generous rate limits than the real-time API.

**Tip:** In multi-service architectures, assign a dedicated API key to each service so that one service's rate usage does not exhaust the shared quota for others.

---

## Why does my invoice show a different amount than what was quoted during signup?

Invoice amounts can differ from your original quote for several legitimate reasons: prorated charges from a mid-cycle plan upgrade, seat count changes, API overage fees, or currency conversion for non-USD accounts.

The most common scenario is a prorated charge. If you upgraded your plan partway through a billing cycle, NexaSupport calculates the difference between your old and new plan costs and charges only for the remaining days of the current period. This prorated amount appears as a line item labeled Plan Upgrade Proration on your invoice. You can verify the calculation by checking Billing > Documents > [Current Invoice] and reviewing the line item breakdown.

Seat overages occur when your active user count exceeds the seat allocation included in your plan. For example, if your Growth plan includes 25 seats and you have 28 active users, the three excess seats are billed at the per-seat overage rate defined in your contract. Review your seat allocation under Billing Overview > Seat Utilization.

API overage charges apply on Starter plans when request volumes exceed monthly API call limits. These appear as a separate line item under API Usage. Growth and Enterprise plans do not incur per-call overage fees but may be subject to rate limiting.

If you believe an invoice contains an error, navigate to Billing > Documents, open the invoice in question, and click Report an Issue. Your billing team will review the dispute within two business days and issue a credit memo if warranted.

**Note:** Annual contracts lock in pricing for the contract period, but seat changes and overages may still generate mid-cycle charges. Review your contract's overage terms in Billing > Contract Details.

---

## How do I update my payment method or billing contact before the next invoice?

Payment method updates and billing contact changes can be made at any time from the Billing settings panel without contacting support.

To update your payment method, navigate to Billing > Payment Methods and click Add Payment Method. NexaSupport supports major credit and debit cards, ACH bank transfers (US accounts only), and wire transfer for Enterprise contracts. After adding the new payment method, click Set as Default to ensure future invoices are charged to the updated method. The old payment method remains saved but inactive until you remove it manually.

If a previous payment failed, you will see a Payment Requires Action banner at the top of the Billing page. After updating the payment method, click Retry Payment to immediately attempt the overdue charge rather than waiting for the automated retry cycle (which attempts payment every 72 hours up to three times before suspending the account).

To update the billing contact — the email address that receives invoices, payment confirmations, and dunning notices — navigate to Billing > Billing Settings and edit the Billing Email field. You can add multiple billing contacts by separating email addresses with commas. This field does not need to match any active workspace user account, making it easy to route invoices directly to your finance team.

For Enterprise accounts on invoiced billing, changes to purchase order numbers, VAT registration details, or billing address should be communicated to your account manager, as these changes may require a contract amendment before they appear on future invoices.

**Tip:** Set a billing contact that is a shared team mailbox (e.g., finance@yourcompany.com) rather than an individual's email to avoid missed invoices when team members leave.

---

## Can I downgrade my plan and what happens to my data?

Plan downgrades are supported but they carry important implications for feature access, seat limits, and data retention that you should understand before proceeding.

To request a downgrade, navigate to Billing > Plan & Usage and click Change Plan. Select the lower tier and review the impact summary, which will highlight which features you will lose access to, how your seat limit will change, and whether any integrations will be disabled. Downgrades do not take effect immediately — they are scheduled for the start of your next billing cycle unless you are on a month-to-month plan, in which case the change can be applied with five days notice.

Feature access changes that commonly affect downgrading customers include: loss of advanced analytics dashboards (not available on Starter), reduction in API rate limits, disabling of SSO authentication (Enterprise-only), and removal of custom routing rule limits. Any automations or workflows that rely on features not available on the target plan will be paused automatically and flagged with a warning icon in the Automation panel.

Your historical ticket data, customer records, and configuration settings are preserved during a downgrade and remain accessible according to the retention policy of your new plan tier. Starter plans retain ticket data for 12 months, Growth plans for 24 months, and Enterprise plans for configurable periods up to seven years.

If you are considering downgrading due to cost concerns, contact your account manager before confirming. NexaSupport frequently offers mid-cycle adjustments, temporary credits, or reduced seat packages that can lower your invoice without losing access to critical features.

**Note:** Downgrading from Enterprise to Growth or Starter will remove any negotiated custom SLA agreements, dedicated support access, and data residency configurations. These cannot be restored without a new Enterprise contract.

---

## Why is my Salesforce sync not updating NexaSupport records after I make changes in Salesforce?

If changes made in Salesforce are not appearing in NexaSupport, the most likely causes are: the OAuth token used for the integration has expired, the Salesforce user account that authorized the connection no longer has API permissions, or the sync frequency is set to a long interval and the update simply has not triggered yet.

Start by navigating to Integrations > Marketplace > Salesforce > Configure and checking the Last Sync Status field. If it reads "Authorization Required" or "Token Expired," click Reconnect and re-authorize the OAuth flow using a Salesforce account with full API access (System Administrator profile recommended). After reconnecting, click Force Sync Now to immediately pull the latest data.

If the status shows "Sync Running" but records are still not updating, check the field mapping configuration. It is possible that the Salesforce field you changed is not included in the NexaSupport field mapping. For example, if you updated the Renewal Date in Salesforce but the Opportunity Close Date → Renewal Date mapping was never configured, the change will not propagate. Add the missing field mapping under the Configure panel and run another forced sync.

Also confirm that the Salesforce record type being modified matches the object mapped in NexaSupport. If your integration is configured to sync Contacts but the change was made on a Lead record, that change will not trigger a sync.

For bi-directional sync configurations, verify that the conflict resolution policy is set appropriately under Sync Settings > Conflict Handling. If Salesforce Always Wins is enabled, NexaSupport changes will not propagate back to Salesforce and vice versa.

**Tip:** After any Salesforce org changes — such as field permission updates, profile changes, or connected app modifications — always revalidate the NexaSupport integration from the Integrations > Marketplace panel to catch newly introduced sync errors early.

---

## How does NexaSupport sync ticket data back to HubSpot and what gets written?

NexaSupport supports bi-directional sync with HubSpot, meaning that ticket events created or updated in NexaSupport can be written back to HubSpot as Timeline Activities on the associated contact and company records.

When bi-directional sync is enabled, the following ticket events are written to HubSpot: ticket created, ticket status changed (e.g., open → resolved), ticket assigned to agent, SLA breach, and ticket closed with resolution. Each event appears in HubSpot's contact or company timeline as a NexaSupport Activity card showing the ticket ID, subject, status, assigned agent, and a link back to the full ticket in NexaSupport.

To enable this, navigate to Integrations > Marketplace > HubSpot > Configure and toggle on Write Ticket Events to HubSpot Timeline. Select which event types you want to sync using the event filter checkboxes. Note that only ticket events linked to a requester email that matches a HubSpot contact will sync — tickets from unrecognized email addresses will be skipped unless you enable the Create New HubSpot Contacts option in the advanced settings.

The sync does not overwrite or modify existing HubSpot deal stages, lifecycle statuses, or contact properties — it only appends timeline activity records. If you want to update HubSpot deal or contact properties based on NexaSupport ticket data (e.g., update a custom "Last Support Date" field), configure a NexaSupport Workflow with a HubSpot Update action, which is available under Settings > Automation > Workflows for Growth and Enterprise customers.

**Note:** HubSpot API quotas are shared across all connected applications in your HubSpot portal. If your portal is already near its daily API call limit, NexaSupport sync writes may be throttled. Monitor HubSpot API usage from your HubSpot portal's API Usage dashboard.

---

## Why is there a delay when ticket data appears in my CRM after resolution in NexaSupport?

Sync delay between NexaSupport and your CRM is normal to varying degrees depending on your sync configuration, CRM API response times, and the volume of events being processed.

For real-time sync configurations, typical delivery latency is under 60 seconds under normal load. During peak usage periods or following bulk ticket operations, latency may extend to 2–5 minutes due to queue processing. This is expected behavior and does not indicate a configuration problem.

For scheduled sync configurations (15-minute, 30-minute, or 60-minute intervals), records will only update in your CRM at the next scheduled sync window. If you need a specific record updated immediately, navigate to Integrations > Marketplace > [CRM Name] > Configure and click Force Sync Now to trigger an out-of-schedule sync.

If delays are consistently exceeding your expected window, check the Integration Health dashboard under Integrations > Marketplace > [CRM Name] > Health. Look for elevated Error Rate percentages, which indicate that sync attempts are failing silently rather than delivering. Each failed sync attempt is logged with a reason code; common causes include CRM API timeouts, field validation failures in the CRM, and rate limit throttling from the CRM provider.

Enterprise customers using bi-directional sync with conflict handling enabled should also check whether a conflict resolution rule is blocking writes for certain record types. Blocked writes do not generate error alerts by default — enable Write Conflict Notifications under Sync Settings to receive alerts when a write is suppressed.

**Tip:** Set your CRM sync frequency to Real-Time during the first two weeks after go-live so you can validate that all field mappings are working correctly before switching to a scheduled interval.

---

## How do I set up ticket routing rules so that Enterprise customers always get assigned to senior agents?

Routing rules in NexaSupport support customer tier-based conditions, which makes it straightforward to prioritize Enterprise accounts.

Navigate to Settings > Automation > Routing Rules and click Create Rule. In the Conditions section, click Add Condition and select Customer Tier from the field dropdown. Set the operator to Equals and the value to Enterprise. This condition will match any incoming ticket where the requesting customer is identified as an Enterprise account in NexaSupport, either through direct account record linking or via CRM sync.

In the Actions section, set the assignment type to Assign to Team and select the team you have designated for senior agents (e.g., "Tier 2 Support" or "Enterprise Success"). Choose Load-Balanced as the assignment method to distribute evenly across team members rather than always assigning to the first available agent.

Also set Priority to High or Urgent for Enterprise tickets in the same rule. This ensures that even if an Enterprise ticket is briefly sitting in queue, it surfaces above non-Enterprise tickets in all agent views.

Save the rule and then drag it to the top of your routing rules list, above any broader catch-all rules. Routing rules are evaluated sequentially, so higher-priority rules should always be placed higher in the list.

To verify the rule is working, use the Route Simulator at the bottom of the Routing Rules panel. Enter customer_tier = Enterprise and a sample subject line, then click Simulate to confirm the rule fires and routes to the correct team.

**Note:** If the Customer Tier field on an incoming ticket is blank (which can happen when tickets arrive via direct email from unknown addresses), the Enterprise routing rule will not fire. Configure a fallback rule below it to handle unidentified customers.

---

## What happens to SLA timers when a ticket is waiting on the customer for a response?

SLA timers in NexaSupport are affected by ticket status changes, and you can configure the platform to pause SLA countdowns during periods where your team is waiting on a customer reply.

When an agent sets a ticket status to Pending — which conventionally means "waiting for customer response" — NexaSupport automatically pauses both the First Response Time and Resolution Time SLA timers if your SLA policy has the Pause on Pending toggle enabled. Navigate to Settings > SLA Policies > [Your Policy] > Advanced Settings and confirm this toggle is active.

Once the customer replies, NexaSupport detects the inbound message event and automatically transitions the ticket status back from Pending to Open. At that moment, the SLA timer resumes from where it was paused, not from zero. This preserves an accurate picture of agent responsiveness while giving your team credit for time spent waiting on the customer.

If you want finer control over which status transitions pause SLA timers, Enterprise customers can define custom statuses under Settings > Ticket Statuses and configure individual SLA pause behaviors for each one. For example, you could create an "Escalated to Engineering" status that also pauses the SLA timer since resolution is blocked pending a third-party fix.

For reporting purposes, time spent in Pending status is tracked separately in the SLA Compliance Report under Analytics > SLA. The report breaks down total ticket duration, active SLA time, and paused time so that managers can evaluate agent performance without penalizing them for customer response delays.

**Tip:** Train agents to consistently use the Pending status rather than leaving tickets Open with no activity. This keeps SLA compliance metrics accurate and flags tickets that have been waiting too long for a customer reply via the Stale Pending Tickets report.

---

## How do I create an automation that sends a follow-up email to a customer 3 days after ticket resolution?

Post-resolution follow-up automations are a common use case and are fully supported through NexaSupport's Workflow builder.

Navigate to Settings > Automation > Workflows and click New Workflow. Set the trigger event to ticket.status_changed. In the trigger condition filters, set Status Changed To = Resolved. This fires the workflow whenever a ticket transitions to resolved status.

Next, add a Wait step by clicking Add Action > Wait. Set the duration to 3 days. After the wait step, add a Send Email action. Select the recipient as Ticket Requester and choose a reply template from your saved templates library, or compose the message inline. Use dynamic variables such as {{customer_name}}, {{ticket_id}}, and {{agent_name}} to personalize the message. A common follow-up message confirms the resolution, asks whether the issue has recurred, and includes a link to submit a new ticket if needed.

Add a condition before the Send Email step to check that the ticket status is still Resolved at the time of sending. This prevents the follow-up from firing if the customer reopened the ticket within the three-day window. Add a Condition step with: Current Status = Resolved. If the condition is not met, set the branch to End Workflow.

Save and activate the workflow. You can monitor delivery status and workflow execution history from the Workflow Runs log at the bottom of the workflow editor. Each execution shows the trigger event, the steps completed, and the timestamp of each action.

**Note:** Workflows that include Wait steps count against your active workflow quota. Starter plans support up to 10 active workflows, Growth plans up to 50, and Enterprise plans have no limit. If you are near your quota, consider deactivating unused workflows before creating new ones.
