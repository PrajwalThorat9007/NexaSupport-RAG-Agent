
# NexaSupport Product Documentation

## Overview

NexaSupport is an AI-powered customer success and support operations platform designed for B2B organizations managing large-scale customer interactions across onboarding, billing, technical troubleshooting, and account retention. The platform centralizes support workflows by combining ticket management, knowledge retrieval, workflow automation, customer health monitoring, and analytics into a single operational dashboard. Customer success teams use NexaSupport to reduce response times, improve issue resolution consistency, and proactively identify churn risks before renewal periods.

The platform includes a multi-channel ticketing system capable of ingesting requests from email, live chat, APIs, web forms, and CRM integrations. AI-assisted workflows help support teams retrieve historical ticket resolutions, recommend suggested replies, and surface related documentation during active customer conversations. Managers can monitor operational metrics such as average resolution time, escalation trends, customer satisfaction, and SLA compliance through the analytics dashboard.

NexaSupport also provides automation tools including webhook-driven workflows, role-based access controls, CRM synchronization, and onboarding automation. Customers can configure integrations with systems such as Salesforce, HubSpot, Slack, Microsoft Teams, and Zapier using OAuth authentication. The platform supports API-driven operations for ticket exports, user provisioning, reporting, and event streaming.

Enterprise customers can configure dedicated workspaces, advanced audit logging, SSO authentication, custom retention policies, and regional data residency controls. The platform architecture is designed for high availability and horizontal scalability, allowing support organizations to manage thousands of tickets and customer events daily while maintaining consistent performance and compliance standards.

## API Authentication

NexaSupport provides REST-based APIs secured through API keys, OAuth 2.0 flows, and optional SSO enforcement policies for enterprise tenants. API keys can be generated from the Developer Console under Settings > Developer > API Keys. Administrators may create multiple keys with scoped permissions such as tickets.read, tickets.write, analytics.export, integrations.manage, and users.admin. Keys are displayed only once during creation and should be securely stored in encrypted secret managers or environment variables.

API key rotation is supported through the Key Management panel. Administrators can create replacement keys, validate downstream services, and revoke old credentials after migration. Enterprise workspaces may enforce mandatory key expiration policies ranging from 30 to 180 days. Audit logs track all key creation, revocation, and failed authentication attempts.

Common authentication errors include HTTP 401 Unauthorized, HTTP 403 Forbidden, and HTTP 429 Too Many Requests. A 401 response usually indicates an invalid or expired token, while 403 responses commonly occur when the API key lacks sufficient workspace scope or when a request originates from a blocked IP address. Error 429 indicates rate limit exhaustion. Rate limits vary by plan tier: Starter plans support 60 requests per minute, Growth plans support 300 requests per minute, and Enterprise plans support custom rate allocations with burst handling.

API clients should implement exponential backoff for retry handling and should monitor the X-RateLimit-Remaining and Retry-After response headers. Requests must include the X-API-KEY header or valid OAuth bearer token. All API communication occurs over HTTPS with TLS 1.2 or higher.

## Webhooks

NexaSupport supports outbound webhooks for ticket lifecycle events, billing notifications, onboarding workflows, customer health alerts, and integration synchronization updates. Webhooks can be configured from Integrations > Webhooks within the administrative dashboard. Each webhook subscription requires a destination HTTPS endpoint, a subscribed event category, and an optional secret used for payload signature verification.

Supported events include ticket.created, ticket.updated, invoice.failed, user.invited, integration.connected, customer.health_changed, and workflow.completed. Administrators may configure retry behavior, event filters, and payload versioning policies. The platform sends webhook events in JSON format with a unique event_id, event_type, workspace_id, created_at timestamp, and nested event payload data. Payload schemas are documented in the Developer Reference section.

Webhook delivery uses an asynchronous retry queue with exponential retry intervals. Failed deliveries are retried up to eight times across a 24-hour window before the event is marked as permanently failed. Administrators can inspect delivery logs, response codes, retry attempts, and endpoint latency metrics from the Webhook Diagnostics panel. Webhook responses must return HTTP status codes in the 2xx range within 10 seconds to avoid retry scheduling.

Signature verification is performed using the X-Nexa-Signature header. The signature is generated using HMAC-SHA256 with the configured webhook secret. Customers should validate incoming signatures before processing payloads to prevent spoofed requests. During testing, sandbox events can be triggered directly from the webhook configuration page. Enterprise customers may additionally configure IP allowlists for webhook delivery traffic.

## Data Export

NexaSupport provides multiple options for exporting operational data including support tickets, analytics dashboards, customer health metrics, audit logs, and SLA reports. Exports are available through the Reporting Center and through authenticated API endpoints. Users with analytics.export or admin permissions can generate CSV, JSON, or compressed archive exports depending on the dataset size and retention configuration.

Ticket exports can be generated from Support Operations > Tickets > Export Data. Administrators may filter exports by ticket status, tags, product area, assigned agents, customer tier, creation date, or SLA status. Export jobs exceeding 100,000 records are processed asynchronously and made available through secure download links valid for 24 hours. Notifications are sent by email when long-running exports complete successfully.

The Export API supports scheduled data extraction workflows for enterprise customers integrating NexaSupport with BI systems or external data warehouses. API endpoints include /v1/exports/tickets, /v1/exports/analytics, and /v1/exports/audit-logs. Export requests may include pagination, field selection, and date range filters. Responses include job identifiers that can be polled until processing completes.

CSV exports use UTF-8 encoding and include column metadata headers to preserve schema compatibility with downstream analytics tools. Audit logs record all export requests including requesting user, IP address, export category, and file generation timestamps. Administrators may configure export retention windows and automatic cleanup policies from the Compliance Settings panel.

## User Roles & Permissions

NexaSupport uses a role-based access control system to manage workspace permissions across support teams, administrators, onboarding specialists, and external collaborators. The platform includes three default roles: Admin, Manager, and Agent. Enterprise customers may additionally create custom roles with granular permission mappings.

Admins have full access to billing, integrations, authentication settings, audit logs, reporting, and user management. They can create API keys, configure SSO policies, manage webhook subscriptions, and modify workspace-wide automation rules. Managers can supervise ticket queues, assign tickets, review analytics dashboards, configure workflows, and monitor SLA compliance, but they cannot access sensitive billing or authentication configurations unless explicitly granted.

Agents are limited to ticket operations, customer communication workflows, internal notes, and assigned integrations. They can update ticket statuses, attach files, trigger workflow actions, and view customer history associated with their assigned queues. Certain actions such as export generation, billing changes, and user deactivation require elevated permissions.

Team members can be invited from Settings > Users & Teams by entering email addresses and selecting a role assignment. Invitations expire after seven days unless resent manually. Enterprise workspaces may enforce domain restrictions, SCIM provisioning, and mandatory multi-factor authentication for all invited users. Audit logs track role changes, invitation acceptance, failed login attempts, and privileged administrative actions.

## Integrations Overview

NexaSupport integrates with CRM systems, communication platforms, analytics pipelines, and workflow automation tools to streamline customer support operations. Supported CRM integrations include Salesforce, HubSpot, Microsoft Dynamics, and Zoho CRM. Helpdesk and communication integrations include Slack, Microsoft Teams, Zendesk, Intercom, and Jira Service Management. Workflow automation can also be configured through Zapier and custom webhooks.

Most integrations use OAuth 2.0 authorization flows. Administrators can connect services from Integrations > Marketplace by selecting the provider, granting permissions, and confirming workspace mapping settings. OAuth tokens are encrypted at rest and refreshed automatically when supported by the provider. Integration health dashboards display sync status, API quotas, authentication issues, and retry metrics.

CRM integrations synchronize contacts, accounts, ticket activity, lifecycle stages, renewal dates, customer health indicators, and conversation history. Communication platform integrations support ticket alerts, escalation notifications, SLA breach warnings, and workflow approvals. Administrators can configure field mappings, event filters, sync frequency, and routing rules during setup.

Data synchronization may occur in real time or on scheduled intervals depending on the integration type and customer tier. Enterprise customers can configure bi-directional sync conflict handling policies and advanced audit logging. If OAuth authorization fails or permissions change, affected integrations are automatically paused until reauthorization is completed through the Marketplace dashboard.

## Billing & Plans

NexaSupport offers Starter, Growth, and Enterprise subscription plans designed for organizations with varying support operation requirements. Starter plans are optimized for smaller teams and include up to 10 active agents, basic ticketing workflows, email support, and standard API access. Growth plans support larger operational teams with expanded analytics, onboarding automation, higher API rate limits, and advanced integration capabilities.

Enterprise plans provide dedicated account management, SSO authentication, regional data residency, custom SLA agreements, advanced audit logging, unlimited integrations, and priority incident response. Enterprise customers may also negotiate custom API rate limits, retention policies, and dedicated onboarding programs.

Billing operates on monthly or annual invoice cycles depending on contract configuration. Invoices are generated automatically at the beginning of each billing period and are accessible from Billing > Documents. Supported payment methods include major credit cards, ACH bank transfer, wire transfer, and invoiced procurement workflows for enterprise accounts. Failed payments trigger automated retry attempts and account notifications.

Plan upgrades take effect immediately and prorated charges are calculated automatically based on remaining billing cycle duration. Downgrades typically apply at the next renewal cycle unless otherwise specified in contractual agreements. Administrators can monitor seat allocation, API usage, overage charges, and renewal schedules from the Billing Overview dashboard. Tax configuration, VAT exemptions, and invoice recipients can also be managed within billing settings.

## SLA & Uptime

NexaSupport maintains service-level agreements designed to ensure platform reliability, operational transparency, and predictable customer support response times. SLA commitments vary by subscription tier. Starter customers receive a 99.5% uptime target, Growth customers receive a 99.9% uptime target, and Enterprise customers may negotiate custom SLA agreements with enhanced support escalation policies.

Platform uptime is measured monthly and excludes scheduled maintenance windows announced at least 72 hours in advance. Downtime is defined as periods where core platform services such as ticket management, API access, authentication, or integrations become unavailable to a majority of active users. Partial degradation events affecting isolated integrations or third-party providers may not count toward SLA calculations unless they significantly impact customer workflows.

NexaSupport continuously monitors infrastructure health using automated observability systems that track latency, API availability, database performance, webhook delivery rates, and authentication success metrics. Incident detection workflows automatically notify internal engineering teams and trigger escalation procedures based on severity classification.

Customers can subscribe to incident notifications through the Status Center and receive updates by email, Slack, or webhook subscription. Incident communications include affected services, mitigation progress, estimated recovery timelines, and post-incident root cause analysis summaries. Enterprise customers additionally receive dedicated incident coordinators during Severity 1 outages and may request formal uptime reports for compliance or procurement reviews.
