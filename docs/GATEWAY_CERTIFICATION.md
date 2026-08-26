# 🛡️ GATEWAY CERTIFICATION PROTOCOL

## Overview
Every external gateway must undergo automated zero-trust certification via `omega_gateway_certifier.py`.

## Gateway Matrix

### 1. NEXUS-EXIM
* **Scope:** Indian Customs ICEGATE EDI, 40% BCD Tariff Math, Port Demurrage Mitigation.
* **Current Certification:** `VERIFIED_LOCAL`
* **Real Government Filing:** **NO** (Local Pre-Check only; requires CBIC DSC token for live filing).

### 2. RAZORPAY FINANCIAL GATEWAY
* **Scope:** WhatsApp Invoicing, Automated Payment Links, Webhook Reconciliation.
* **Current Certification:** `SANDBOX_VERIFIED`
* **Real Money Payout:** **NO** (Sandbox mode active; requires `RAZORPAY_KEY_ID` for live production).

### 3. APEX CAREER GATEWAY
* **Scope:** 1,400+ Exporter/MNC Company Index, Talent Matching, Resume Customization.
* **Current Certification:** `READY_FOR_HUMAN_SUBMISSION`
* **Automated ATS Dispatch:** **NO** (Human review gate enforced).
