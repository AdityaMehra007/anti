# VENTURE 03: BENGALURU FRESHER & STUDENT CAREER OS (SPEC & ECONOMICS)

**Venture ID:** `VENTURE-BLR-CAREER-2026`  
**Target Market:** 150,000+ Undergraduate & Graduate Students across Bengaluru Tech & Commerce Hubs  
**Value Proposition:** 100% Grounded, Deduplicated Career Intelligence, ATS Resume Alignment, and Recruiter Requisition Matching  
**Operating Status:** Architectural Blueprint & Prototype Validated  

---

## 1. The Core Problem & Market Reality

1. **Unemployment & Noisy Portals:** Over 70% of business and technical graduates apply blindly to generic LinkedIn/Naukri portals, facing 98% rejection rates from ATS keyword misalignment.
2. **Hidden Sales Quotas:** Job portals frequently misclassify cold-calling telemarketing jobs as "Business Operations Associate" or "Management Trainee," trapping freshers in high-churn sales mills.
3. **Agency Intermediary Bloat:** Candidates rarely reach in-house talent acquisition teams with exact requisition numbers.

---

## 2. Product Solution Architecture

The **Bengaluru Fresher Career OS** provides:
1. **Curated MNC & GCC Corridor Board:** Live, verified tracks across Whitefield, Electronic City, Bellandur, and Outer Ring Road corridors (Accenture, EY, JPMorgan, Goldman Sachs, Target, Amazon).
2. **Deterministic 6-Factor Suitability Engine:** BBA/B.Com/B.Tech-specific rubric filtering out hard sales roles and senior experience traps.
3. **One-Click Truth-Layer Resume Formatter:** Produces single-column, ATS-verified DOCX/PDF resumes.
4. **Direct Recruiter & Alumni Requisition Outreach:** Formats personalized messages referencing verified requisition IDs.

---

## 3. Financial Model & Unit Economics (One-Person Lab)

```
[Phase 1: Free Tier Community Engine]  ──> 1,000 Active Student Users (WhatsApp / College Hubs)
                         │
[Phase 2: Freemium Career Vault]      ──> ₹499 / Lifetime or ₹99 / Month for Deep Matching
                         │
[Phase 3: B2B Campus Recruitment API] ──> ₹15,000 / Campus Drive for Verified Screening
```

| Metric | Phase 1 (Months 1–3) | Phase 2 (Months 4–6) | Phase 3 (Months 7–12) |
| :--- | :--- | :--- | :--- |
| **Active Users** | 1,000 | 5,000 | 25,000 |
| **Paid Conversion (3%)** | 0 (Free Beta) | 150 users @ ₹499 = **₹74,850** | 750 users @ ₹499 = **₹3,74,250** |
| **Server / Infrastructure Cost** | ₹0 (GitHub Pages + SQLite + Local) | ₹1,500/mo (Vercel / Supabase Free) | ₹5,000/mo (Managed Cloud) |
| **Gross Margin** | 100% | **96.0%** | **95.5%** |
| **Customer Acquisition Cost (CAC)**| ₹0 (College clubs, DSU alumni network) | ₹50 / user | ₹40 / user |

---

## 4. Immediate Validation Experiment (7-Day Sprint)

1. **Day 1–2:** Export top 20 verified Bangalore Business Operations tracks from `career_vault.db` to a clean public Notion / HTML directory.
2. **Day 3–4:** Share with 50 Dayananda Sagar University final-year BBA peers for resume tailoring feedback.
3. **Day 5–6:** Measure feedback: Did the ATS resume bullets improve interview shortlist rates?
4. **Day 7:** Decision gate: If $\ge 20$ students request automated resume tailoring, deploy local web cockpit to Vercel/GitHub Pages.
