# WORKFLOW SPECIFICATION: EventOps Vendor Rate Audit & SLA Enforcement Loop
**File**: `workflows/eventops_vendor_sla_audit_loop.md`  
**Domain**: Event Operations, Vendor Procurement & Cost Optimization  
**Status**: APPROVED & SPECIFIED (Definition of Done Met)  
**Implementation Seam**: `e:/anti/AI-Command-Center/startup-lab/rate_card_optimizer.py` & `e:/anti/AI-Command-Center/startup-lab/event_logistics_tracker.py`

---

## 1. Loop Profile & Overview
- **Objective**: Automate vendor quotation audits, price inflation detection, milestone delay tracking, and contractual SLA penalty calculations for live corporate events and conferences in Bengaluru (100–3,000+ attendees).
- **Core Problem Solved**: Event vendors frequently levy unstandardized 20–35% rush surcharges, opaque equipment rental rates, and stage handover delays that erode event gross margins.
- **Ground Truth**: Benchmarked against verified Bengaluru market rate cards and Aditya Mehra's operational track record (300+ events delivered, 15–20% procurement cost reduction, zero budget overruns).
- **Output Brief**: Itemized audit report with line-item markup flags, SLA delay penalty ledger, and pre-formulated counter-negotiation letter.

---

## 2. Trigger
- **Mechanism**: Event-Driven File Drop or CLI Execution.
- **Trigger Conditions**:
  1. *File Drop Event*: When a vendor quotation JSON or structured CSV is placed into `startup-lab/incoming_quotes/`.
  2. *On-Demand Command*: Execution of `python startup-lab/rate_card_optimizer.py --audit <path_to_quote>`.
  3. *Milestone SLA Event*: Execution of `python startup-lab/event_logistics_tracker.py --delay <vendor_id> <hours>`.

---

## 3. Autonomous Execution Pipeline (Pre-Checkpoint)

All analytical computations occur autonomously before presenting the brief:

1. **Quotation Ingestion & Normalization**:
   - Parse line items: `item_name`, `quantity`, `quoted_unit_rate`, `vendor_name`, `category` (AV, Staging, Fabrication, Power, Catering).
2. **Benchmark Rate Card Matching**:
   - Match line items against verified Bengaluru master benchmark rates in `RateCardOptimizer`:
     - Octanorm / German Hanger Tent Structure: Rs 18.00 / sq ft
     - Line Array Audio Rig & Digital Mixer: Rs 35,000 / day
     - 4K P2.6 Indoor LED Wall: Rs 120.00 / sq ft
     - 125 kVA Silent DG Generator: Rs 12,000 / shift
     - Truss Staging & Wooden Platform: Rs 32.00 / sq ft
3. **Markup & Inflation Calculation**:
   - Compute variance: $\Delta = \text{Quoted Rate} - \text{Benchmark Rate}$.
   - Flag all line items where $\Delta > 10\%$.
   - Calculate potential gross cost savings in INR and percentage.
4. **Milestone SLA Delay Audit** (if milestone completed post-deadline):
   - Compute contractual hourly delay penalty (5% per hour of handover delay, capped at 30% contract value).
   - Compute final net payable expenditure: $\text{Payable} = \text{Contracted} - \text{Penalty}$.
5. **Counter-Proposal Letter Generation**:
   - Automatically draft a professional vendor counter-negotiation letter citing specific inflated line items and offering a standardized master rate card.

---

## 4. Checkpoint (Push-Right)

The checkpoint is pushed to the final decision. The human does not perform manual Excel math or draft letters from scratch.

### The Decision-Ready Brief
- **Surface**: Console output, markdown report in `startup-lab/audits/`, and JSON telemetry.
- **Brief Contents**:
  - **Quotation Summary**: Vendor Name, Event Name, Total Quoted Amount (INR), Total Benchmark Cost (INR).
  - **Gross Savings Identified**: Net savings in INR and percentage (e.g. *Rs 38,500 identified — 21.7% savings*).
  - **Inflated Line Items**: Table showing Item, Quantity, Quoted Rate, Benchmark Rate, and Variance %.
  - **SLA Penalties (if any)**: Delay hours, contractual penalty deduction, and final net payable.
  - **Ready-to-Send Counter-Letter**: Complete text ready to paste into email or WhatsApp.

### Human Action
1. Review brief (30 seconds).
2. Approve counter-offer or adjust target margin.
3. Send pre-drafted negotiation letter to vendor.

---

## 5. Failure Modes & Edge Case Recovery

| Failure Mode | Autonomous Handling | Fallback |
| :--- | :--- | :--- |
| **Unrecognized Line Item** | Item not in master benchmark. | Flag item as *"Unclassified Specialty Item"*; compute audit on matched subset only. |
| **Vendor Dispute on Penalty** | Contract clause ambiguity. | Output standardized cure window timeline and secondary backup vendor quotes. |
| **Malformed Quotation Format** | Missing required keys (`item_name`, `quoted_unit_rate`). | Return validation error with missing field names without corrupting ledger. |

---

## 6. Definition of Done & Verification Criteria
- [x] Deterministic calculation: Verified by automated test case `TC-07` in `tests/test_career_engine.py` (21.7% inflation detected).
- [x] SLA penalty calculation: Verified by automated test case `TC-09` in `tests/test_career_engine.py` (Rs 20,000 penalty deducted accurately).
- [x] Production code ready: `startup-lab/rate_card_optimizer.py` and `startup-lab/event_logistics_tracker.py` execute cleanly with 0 dependencies.
- [x] Zero ambiguities remaining: An implementer can maintain and extend the master rate card independently.
