# NexaSupport Onboarding Guide

## Welcome to NexaSupport

Congratulations on joining NexaSupport. This guide will walk you through everything your team needs to get fully operational within your first 30 days. Whether you are setting up a small support team or rolling out the platform across a large enterprise, each step is designed to build on the previous one so nothing is skipped or misconfigured.

In your first week, you will complete account setup, invite your team, and connect your existing CRM. By the end of week two, most teams have imported historical tickets and configured their routing rules. Week three focuses on automations, SLA timers, and business hours configuration. In week four, you will train your agents, run a pilot batch of live tickets, and confirm that all integrations are syncing correctly.

Your dedicated onboarding specialist is listed under Settings > Account > Onboarding Contact. You can schedule calls directly through the in-app calendar widget. For async questions, the NexaSupport Help Center is available 24/7 and includes video walkthroughs of every step in this guide.

A few things to keep in mind as you begin: only users with the Admin role can complete the setup steps in this guide. If you are an agent or manager who needs to reference this document, coordinate with your workspace administrator before attempting configuration changes. Also ensure that the email domain used during account creation matches the domains of teammates you plan to invite, especially if your organization enforces domain-based access controls.

At the end of the 30-day onboarding window, NexaSupport automatically runs a health check on your workspace configuration and sends a summary report to your registered admin email. This report identifies incomplete setup steps, misconfigured integrations, and agents who have not yet logged in.

---

## Step 1: Account Setup

Before inviting your team or connecting integrations, take a few minutes to complete the core account configuration. This ensures your workspace reflects your organization's identity and operational preferences from day one.

1. **Complete your Admin profile.** Navigate to Settings > Profile and fill in your full name, job title, and contact email. Upload a profile photo if desired. This information appears in customer-facing ticket communications, so accuracy matters.

2. **Set your workspace name and timezone.** Go to Settings > Workspace > General. Enter your company name as it should appear in ticket headers and email notifications. Set the primary timezone to match your main support team's location. If your team spans multiple time zones, you will configure per-agent timezone overrides in Step 6.

3. **Configure notification preferences.** Under Settings > Notifications, choose how the platform alerts you to new tickets, SLA breaches, escalations, and billing events. Options include in-app notifications, email digests, and Slack alerts (requires Slack integration from Step 2). For high-volume teams, we recommend enabling email digests rather than per-event emails to avoid inbox overload.

4. **Invite team members.** Navigate to Settings > Users & Teams and click Invite Members. Enter each teammate's email address and assign a role: Admin, Manager, or Agent. New invitations expire after seven days. You can resend expired invitations from the Pending Invitations tab. For enterprise workspaces with SCIM provisioning enabled, skip this step and manage user provisioning through your identity provider instead.

5. **Create your first team.** Teams group agents for routing and reporting purposes. Under Settings > Users & Teams > Teams, click Create Team, name it (e.g., "Billing Support" or "Tier 2 Technical"), and assign members. Teams are referenced later in Step 4 when you configure ticket routing rules.

6. **Enable two-factor authentication.** For security, navigate to Settings > Security > Authentication and toggle on Require 2FA for Admins. Enterprise customers can extend this requirement to all roles.

---

## Step 2: Connect Your CRM

Connecting your CRM is one of the highest-value steps in the onboarding process. It enables automatic customer record lookup during ticket creation, bi-directional data sync, and health signal enrichment on the customer dashboard.

### Connecting Salesforce

1. Navigate to **Integrations > Marketplace** and click on the Salesforce tile.
2. Click **Connect Salesforce** and you will be redirected to Salesforce's OAuth authorization page. Sign in with a Salesforce account that has API access permissions (typically a System Administrator profile).
3. After authorizing, you will be returned to the NexaSupport Marketplace page. The Salesforce tile will now show a green **Connected** badge.
4. Click **Configure** to open the field mapping panel. Map the following fields at minimum: Salesforce Account ID → NexaSupport Company ID, Contact Email → Ticket Requester Email, Opportunity Close Date → Renewal Date. Additional optional fields include ARR, Contract Value, and Health Score.
5. Under **Sync Settings**, choose your sync direction: one-way (Salesforce → NexaSupport) or bi-directional. Set sync frequency to Real-Time or Scheduled (every 15, 30, or 60 minutes).
6. Toggle on **Auto-Tag by Account Tier** to automatically apply customer tier tags (Starter, Growth, Enterprise) to incoming tickets based on the Salesforce Account Type field.
7. Click **Save & Test Sync**. NexaSupport will run a validation sync of the first 50 records. Review any field mapping errors displayed in the Sync Validation Report before confirming.

### Connecting HubSpot

1. From **Integrations > Marketplace**, click the HubSpot tile and select **Connect via OAuth**.
2. Sign in to HubSpot with a Super Admin account. Approve the requested permissions: CRM contacts, companies, deals, and timeline events.
3. After redirect, click **Configure** and map: HubSpot Company ID → NexaSupport Company ID, Contact Email → Ticket Requester Email, Deal Close Date → Renewal Date, Lifecycle Stage → Customer Tier.
4. Enable **Bi-directional Activity Sync** to push NexaSupport ticket events back to HubSpot as Timeline Activities. This provides your sales team with support history visibility inside HubSpot.
5. Save and run a test sync to validate mapping before going live.

---

## Step 3: Import Historical Tickets

Importing historical tickets allows your team to preserve institutional knowledge, train AI-assisted suggestions, and maintain continuity for ongoing customer relationships.

1. **Download the import template.** Go to Support Operations > Tickets > Import and click **Download CSV Template**. The template includes the following required columns: ticket_id, created_date, subject, description, status, requester_email, assignee_email, product_area, tags, resolution, resolution_time_hrs. Optional columns include customer_tier, nps_score, and internal_notes.

2. **Prepare your CSV file.** Open the template in Excel or Google Sheets. Paste your historical ticket data, ensuring that:
   - Dates use the format YYYY-MM-DD
   - Status values match accepted options: open, in_progress, resolved, closed
   - Tags are comma-separated within a single cell (e.g., "403 error, API key, billing")
   - Email addresses match existing workspace user accounts where possible

3. **Upload the file.** Return to Support Operations > Tickets > Import and click **Choose File**. Select your prepared CSV and click **Preview Import**. NexaSupport will scan the file and display a column mapping interface.

4. **Map your columns.** Use the dropdown selectors to match your CSV column headers to NexaSupport field names. If your source data uses different naming conventions (e.g., "case_number" instead of "ticket_id"), map them here. Required fields highlighted in red must be mapped before proceeding.

5. **Review deduplication settings.** NexaSupport checks for duplicates using a combination of requester_email and created_date. Toggle **Skip Duplicate Records** to prevent re-importing tickets that already exist. You can also choose to overwrite existing records if you are re-importing updated data.

6. **Run the import.** Click **Start Import**. Imports with fewer than 10,000 rows complete synchronously and results appear within seconds. Larger files are processed asynchronously; you will receive an email notification when complete. Review the Import Results Summary for skipped rows, field validation errors, or unmatched email addresses.

---

## Step 4: Configure Routing Rules

Routing rules determine how incoming tickets are assigned to agents or teams. Well-configured routing reduces manual triage, improves response time, and ensures tickets always reach the right person.

1. **Open the Routing Rules panel.** Navigate to Settings > Automation > Routing Rules and click **Create Rule**.

2. **Define rule conditions.** Each rule requires at least one condition. Available condition fields include: Product Area, Customer Tier, Ticket Tags, Requester Email Domain, Subject Keywords, and Source Channel (email, API, chat). Conditions can be combined using AND/OR logic.

3. **Set the assignment action.** Choose from: Assign to Specific Agent, Assign to Team (round-robin), Assign to Team (load-balanced), or Set Priority Only. For escalation scenarios, you can also choose Notify Manager.

4. **Configure priority rules.** Priority can be set to Low, Medium, High, or Urgent. Define criteria for Urgent tickets such as customer_tier = Enterprise OR tags contains "outage". Urgent tickets bypass standard queue ordering and surface at the top of all agent views.

5. **Create escalation triggers.** Under Settings > Automation > Escalation Triggers, click **Add Trigger**. Set conditions such as: "If ticket remains unassigned for more than 30 minutes AND priority = High, escalate to Manager and send Slack notification." Multiple escalation levels can be stacked for multi-tier escalation chains.

6. **Set rule priority order.** Routing rules are evaluated top-to-bottom. Drag rules in the Rules List panel to reorder them. More specific rules should appear above broad catch-all rules to prevent incorrect overrides.

7. **Test routing.** Use the **Route Simulator** at the bottom of the Routing Rules panel. Enter sample ticket attributes and click Simulate to see which rule would fire and where the ticket would be assigned.

---

## Step 5: Set Up Automations

Automations reduce manual repetition for your agents and ensure that SLA commitments are consistently enforced. NexaSupport's automation engine supports event-based triggers, time-based timers, and scheduled workflows.

1. **Create auto-reply templates.** Navigate to Settings > Automation > Reply Templates and click **New Template**. Templates support dynamic variables including {{customer_name}}, {{ticket_id}}, {{agent_name}}, {{company_name}}, and {{sla_due_at}}. Set trigger conditions such as "On ticket creation, if source = email, send Acknowledgment Template." Auto-replies are sent immediately after the trigger event fires.

2. **Configure SLA timers.** Go to Settings > SLA Policies and click **Create Policy**. Define First Response Time targets (e.g., Urgent = 1 hour, High = 4 hours, Medium = 8 hours, Low = 24 hours) and Resolution Time targets. Assign policies to customer tiers or specific routing rules. When an SLA timer is about to breach, NexaSupport sends a warning notification to the assigned agent and their manager.

3. **Set business hours.** Under Settings > Business Hours, define your operational schedule by day of week and time range. Tickets created outside business hours have SLA timers paused automatically until the next business day. You can configure up to five distinct business hours profiles and assign them to different teams or routing rules.

4. **Build workflow automations.** Navigate to Settings > Automation > Workflows and click **New Workflow**. Choose a trigger event (e.g., ticket.created, ticket.updated, sla.breached), add condition filters, and define action steps. Actions include: add tag, change status, assign to agent, send email, trigger webhook, or create follow-up task. Workflows can contain multi-step action chains.

5. **Enable smart suggestions.** Under Settings > AI Assistance, toggle on **Suggested Replies**. When enabled, agents see AI-generated reply suggestions drawn from resolved ticket history and product documentation. Suggestions are ranked by relevance score and agents can accept, edit, or dismiss them.

---

## Step 6: Train Your Team

A well-prepared team is the difference between a smooth launch and a chaotic one. Invest time in structured agent onboarding during the final phase of setup.

1. **Assign roles carefully.** Review each team member's role assignment under Settings > Users & Teams. Promote agents who will manage queues or run reports to the Manager role. Keep the Admin role limited to two or three individuals to minimize security risk.

2. **Share the Agent Onboarding Checklist.** NexaSupport provides a built-in checklist accessible from the agent's home dashboard. It includes tasks such as: complete profile, review SLA policy, respond to a test ticket, configure personal notification preferences, and review routing queue assignment. Managers can track checklist completion status from Settings > Users & Teams > Onboarding Progress.

3. **Assign suggested first-week tasks.** For each new agent, create a set of onboarding tickets using the Import feature or manually. These dummy tickets let agents practice responding, updating statuses, adding internal notes, and using macros without impacting real customers.

4. **Run a team walkthrough session.** Schedule a 60-minute live walkthrough using screen sharing. Cover: how to claim tickets from the queue, how to use reply templates, how to escalate a ticket, how to set a ticket to pending, and how to use the knowledge base search. Record the session and store it in your internal documentation for future hires.

5. **Set up personal notification preferences.** Remind each agent to configure their own notification settings from Profile > Notifications. Agents should enable desktop notifications for Urgent ticket assignments and SLA warning alerts at minimum.

6. **Establish a feedback loop.** Create a shared Slack channel or internal notes tag (e.g., "#onboarding-feedback") where agents can flag confusing workflows or missing documentation during their first week. Review this feedback in your Week 2 check-in with your NexaSupport onboarding specialist.

---

## Common Onboarding Issues & Fixes

Despite careful setup, certain issues arise frequently during onboarding. Below are the four most common problems and how to resolve them.

### Issue 1: OAuth Token Error When Connecting CRM

**Symptom:** After authorizing Salesforce or HubSpot, you are redirected back to NexaSupport with an error message: "OAuth token exchange failed. Invalid redirect URI."

**Cause:** The redirect URI registered in your CRM's connected app settings does not match the callback URL NexaSupport sends during the OAuth flow.

**Fix:** In Salesforce, navigate to Setup > App Manager > [Your Connected App] > Edit and update the Callback URL to exactly `https://app.nexasupport.com/oauth/callback`. Ensure there is no trailing slash. In HubSpot, go to Settings > Integrations > Private Apps and confirm the Redirect URL matches the same value. After updating, return to NexaSupport's Integrations > Marketplace and retry the connection. Do not use incognito mode during OAuth flows, as cookie restrictions can interfere with token exchange.

### Issue 2: CSV Import Failure — Field Validation Errors

**Symptom:** After uploading your historical tickets CSV, the Preview Import screen shows red validation errors on multiple rows. Common messages include: "Invalid date format in column created_date," "Unrecognized status value in column status," and "Requester email does not match any workspace contact."

**Cause:** Source data often contains date formats (e.g., MM/DD/YYYY), status labels (e.g., "Closed Won"), or email addresses that do not match NexaSupport's schema requirements.

**Fix:** Open your CSV in Excel or Google Sheets. Use the TEXT() function to reformat dates to YYYY-MM-DD. Replace non-standard status values with accepted ones: open, in_progress, resolved, or closed. For unmatched email addresses, either pre-create the contact records in NexaSupport before importing or leave the requester_email column blank and assign manually after import. Download the error report from the Import Results page for a row-by-row list of failures.

### Issue 3: Webhook Not Firing After Configuration

**Symptom:** You configured a webhook subscription for ticket.created events, but your destination endpoint is not receiving any payloads.

**Cause:** Most commonly, the destination URL returns a non-2xx HTTP status code, the endpoint is not publicly accessible, or the subscribed event category was saved incorrectly.

**Fix:** Navigate to Integrations > Webhooks > [Your Webhook] > Delivery Logs. Review the last attempted delivery and check the HTTP response code returned by your endpoint. If the response is 404 or 5xx, fix the endpoint first. If NexaSupport shows "No deliveries attempted," confirm the event subscription is set to ticket.created (not a similar but different event like ticket.updated). Use the **Send Test Event** button on the webhook configuration page to fire a sample payload and verify receipt. Also confirm the endpoint URL includes `https://` and does not require authentication headers that NexaSupport is not configured to send.

### Issue 4: CRM Sync Delay — Records Not Appearing in NexaSupport

**Symptom:** After connecting your CRM, newly created contacts or updated account records in Salesforce or HubSpot are not appearing in NexaSupport within the expected sync window.

**Cause:** This usually occurs when the sync frequency is set to Scheduled (60 minutes), when the OAuth token has silently expired, or when the CRM user account used for authorization no longer has API access permissions.

**Fix:** Navigate to Integrations > Marketplace > [CRM Name] > Configure and check the Last Sync Status. If the status reads "Authorization Required," click **Reconnect** to re-authorize the OAuth token. If status shows "Sync Running" but records are delayed, switch Sync Frequency from 60 minutes to 15 minutes or Real-Time. If the authorizing CRM user's account was deactivated or their API permissions were revoked, reconnect using a different CRM admin account. You can also manually trigger an immediate sync by clicking **Force Sync Now** from the configuration panel.
