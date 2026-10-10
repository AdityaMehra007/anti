---
name: customer-billing-ops
description: Automated Stripe invoicing, recurring retainer collection, sovereign ledger reconciliation, and cash sweep routines.
---

# SKILL: Customer Billing Operations

## Objective
Eliminate payment friction, collect 100% of setup fees upfront prior to onboarding, and automate monthly retainer billing.

## Execution Directives
1. **Pre-Call Link Generation**:
   - Always have the $3,000 Setup Link and $5,000 Enterprise Link pre-generated before starting discovery calls.
2. **On-Call Settlement Protocol**:
   - When the client agrees to terms, paste the checkout link directly into the meeting chat.
   - Do not disconnect until the Stripe webhook confirms payment settlement (`payment_intent.succeeded`).
3. **Automated Ledger Posting**:
   - Instantly post transaction amounts into `enterprise_crm.db` ledger and trigger client provisioning in `nexus_product.db`.
