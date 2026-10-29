# Original User Request

## 2026-10-24T17:14:27Z

Use a full multi-agent team to parallelize data matching, UI console development, and verification.

Build a comprehensive Bengaluru Job Referral Strike & 1-Click Dispatch Console connecting verified live corporate openings across Bengaluru's tech corridors (Outer Ring Road, Manyata, Bellandur, Whitefield, Domlur) to 1,200+ matched LinkedIn employee and recruiter connections for Aditya Mehra, complete with customized referral dockets, interactive clipboard actions, and approval queue integration.

Working directory: `e:/anti/teamwork_projects/bangalore_referral_strike`  
Integrity mode: development

## Requirements

### R1. Comprehensive Bengaluru Target Matching & Scoring
Extract and rank active Bengaluru job openings spanning Operations, Supply Chain, Advisory/Risk, Trade Finance, and Merchant BD across top employers (Accenture, Deloitte, Goldman Sachs, Amazon, IBM, JPMorganChase, KPMG, PwC, Walmart Global Tech, Delhivery, PhonePe). Match each opening against Aditya Mehra's verified profile and link 3–5 verified 1st/2nd-degree LinkedIn employee and recruiter contacts per company from available career intelligence data.

### R2. Personalized Referral Docket & Message Synthesis
Generate three tailored communication assets for each matched contact:
1. **Connection Request Note**: Strict limit of ≤ 290 characters highlighting mutual Bengaluru context and relevant credentials (DSU BBA '26, Aero India 2025 operations lead, Instawork 99%+ QA).
2. **InMail / Message Referral Ask**: Polite, personalized message asking for an internal referral for the specific job requisition.
3. **Internal Referral Docket**: A 3-bullet proof-of-work summary designed for employees to easily paste into their internal corporate referral portals.

### R3. Interactive 1-Click Dispatch Console
Create a self-contained, responsive HTML/JS web console featuring:
- Corridor and company filter pills.
- 1-click clipboard copy buttons for connection notes, referral asks, and internal dockets with visual feedback.
- 1-click direct link launcher to each contact's LinkedIn profile.
- Persistent contact status tracking (`Pending` → `Contacted` → `Referral Submitted`) saved to browser local storage.

### R4. Canonical Approval Queue Integration
Sync all generated P0/P1 referral actions into `data/approval_queue.csv` and `data/approval_queue.json` without breaking existing schemas, enabling batch visibility and CLI tracking.

## Acceptance Criteria

### Data & Target Integrity
- [ ] Every target role is verified in Bengaluru with a live requisition link or careers portal destination.
- [ ] Every contact entry includes full name, current title, and valid LinkedIn URL.
- [ ] 100% of connection request notes are strictly ≤ 300 characters (zero truncation).
- [ ] All claims strictly match verified credentials in `data/verified_profile.json` (no hallucinated achievements).

### Console & Usability
- [ ] Interactive console runs standalone in modern browsers without external server dependencies.
- [ ] Clipboard copy works seamlessly for all message formats.
- [ ] Contact status transitions persist across browser sessions via local storage.

### Verification Suite
- [ ] An automated test script validates dataset completeness, message length constraints, and approval queue formatting.
