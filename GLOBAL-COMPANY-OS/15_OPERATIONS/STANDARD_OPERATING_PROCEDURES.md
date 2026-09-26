# TradeNexus AI: Standard Operating Procedures (SOPs)

## SOP-01: Exporter Onboarding & Initial Compliance Audit
- **Objective**: Onboard a new mid-market exporter tenant and deliver their first zero-error audit within 24 hours.
- **Trigger**: Exporter signs 30-day pilot agreement or completes self-serve registration.
- **Procedure**:
  1. Intake tenant company details (IEC code, GSTIN, authorized ports of exit e.g. INMAA1, INNSA1).
  2. Request 5 historical commercial export invoices and packing lists in PDF/TXT.
  3. Run batch audit pipeline: `ExporterAuditPipeline.run_cohort_audit()`.
  4. Generate and email the Exporter Compliance Baseline Report highlighting any historical tariff misclassifications or CBAM liabilities.
  5. Schedule 15-minute verification walkthrough call with the Exporter Logistics Head.

---

## SOP-02: Daily Regulatory Gazette Diff & Rule Catalog Ingestion
- **Objective**: Ensure TradeNexus ITC-HS and tariff database is 100% current with Indian DGFT, CBIC, and foreign (EU TARIC / US CBP) trade notices.
- **Trigger**: Scheduled background daemon cycle at 02:00 IST daily.
- **Procedure**:
  1. Automated scraper monitors DGFT public notices (`dgft.gov.in`) and CBIC tariff gazettes.
  2. Parse newly published notifications and compare against current `HSCatalog.DATABASE`.
  3. If tariff rate or export restriction changes are detected:
     - Generate a structured diff report.
     - Strategy Agent evaluates severity.
     - If critical change (e.g. new export duty or SCOMET update), trigger automated advisory alert to all affected exporter accounts.
  4. Commit verified rules update to staging registry.

---

## SOP-03: Tariff Classification Exception Triage
- **Objective**: Resolve low-confidence HS-code matches without stalling container shipments.
- **Trigger**: Product classification confidence score falls below 80.0%.
- **Procedure**:
  1. Engine flags invoice item as `REQUIRES_REVIEW` and isolates the line item.
  2. Anomaly summary sent to Forward Deployed Trade Specialist.
  3. Specialist cross-references WCO Explanatory Notes and General Rules of Interpretation (GRI 1–6).
  4. Specialist approves validated 8-digit classification and provides legal citation.
  5. System records resolution in `system_memory_store.json` to prevent repeated manual interventions.

---

## SOP-04: Pilot to Paid Annual Contract Conversion
- **Objective**: Transition 30-day free/discounted pilot accounts into recurring annual SaaS contracts.
- **Trigger**: Day 21 of active 30-day pilot.
- **Procedure**:
  1. Compile Executive ROI Summary:
     - Total Shipping Bills Audited
     - Total Prevented Demurrage Exposure (\$)
     - Processing Hours Saved
  2. Present Annual Contract Proposal:
     - Standard: ₹25,000/month (billed annually at ₹2,70,000 — 10% discount).
     - Scale (with CBAM XML generator): ₹50,000/month (billed annually at ₹5,40,000).
  3. Secure electronic signature and setup automated monthly/annual invoice billing.
