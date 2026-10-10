---
name: speed-to-lead-automation
description: Real-time inbound webhook triage, sub-60-second AI inquiry qualification, and calendar slotting protocols.
---

# SKILL: Speed-to-Lead Automation

## Objective
Respond to all inbound inquiries and email responses in under 60 seconds, driving a 400% higher booking conversion rate compared to standard response times.

## Execution Directives
1. **Webhook Ingestion**:
   - Parse inbound payload immediately for intent keywords (`"pricing"`, `"call"`, `"yes"`, `"demo"`, `"Loom"`).
2. **Dynamic Context Formulation**:
   - Inject the prospect's company name and core pain point into the auto-reply draft.
   - Embed direct calendar booking links (Cal.com / Calendly) with pre-filled email parameters.
3. **Escalation Trigger**:
   - If response contains enterprise-scale keywords (headcount > 100 or budget > $50k), ping the founder's mobile device via urgent webhook in <30 seconds.
