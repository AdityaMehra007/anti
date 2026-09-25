# Multi-Agent Autopilot Architecture & Agent Registry
**System Owner:** Aditya Mehra | BBA International Business (Dayananda Sagar University, Bangalore)

This system establishes a 4-agent autonomous pipeline dedicated to accelerating Aditya Mehra's job acquisition across top MNCs, GCCs, and high-growth companies in Bangalore.

---

## 🤖 Deployed AI Subagent Registry

```
                             [ ADITYA MEHRA AUTOPILOT CORE ]
                                           │
         ┌──────────────────┬──────────────┴───────────────┬──────────────────┐
         ▼                  ▼                              ▼                  ▼
┌──────────────────┐ ┌──────────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  job_scout_agent │ │ resume_cover_letter_     │ │recruiter_outreach│ │mnc_interview_    │
│                  │ │ customizer               │ │_agent            │ │coach             │
└────────┬─────────┘ └────────────┬─────────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                        │                        │                        │
         ▼                        ▼                        ▼                        ▼
 Scans Bangalore MNC    Customizes ATS Resume    Generates LinkedIn Notes,  Drills Incoterms,
 Portals & Updates      & Company Cover Letters  InMails & Cold Emails to   STAR Case Studies
 Application Tracker    for Target Positions     Target HR Recruiters       & Mock Interviews
```

---

## Agent Specifications & Operational Directives

### 1. `job_scout_agent`
- **Purpose:** Identifies active early-career openings, management trainee tracks, and off-campus recruitment drives in Bangalore.
- **Target Companies:** Accenture, Deloitte, EY, KPMG, PwC, Amazon, Goldman Sachs, JP Morgan, IBM, TE Connectivity, Boeing, Puma, Pencil Mark Interior.
- **Target Roles:** Business Development Executive, Global Operations Analyst, Event Operations Coordinator, EXIM & Supply Chain Trainee, Client Relationship Manager.
- **Output:** Automatically records new opportunities in `e:\anti\Application_Tracker.csv`.

---

### 2. `resume_cover_letter_customizer`
- **Purpose:** Customizes ATS-friendly resumes and company-specific cover letters for target job postings in Bangalore.
- **Candidate Data Sources:** `e:\anti\Resume_Aditya_Mehra.md` (Dayananda Sagar University BBA IB, AERO India 2025 Lead, TRILOGY Event Lead, Pencil Mark BD Internship Commendation, Google Digital Marketing, NPTEL Service Marketing & Outskill Generative AI Certifications).
- **Output:** Updates `e:\anti\Resume_Aditya_Mehra.md` and generates customized entries in `e:\anti\Cover_Letters_All_MNCs.txt`.

---

### 3. `recruiter_outreach_agent`
- **Purpose:** Crafts high-converting LinkedIn connection requests (300-char limit), LinkedIn InMail messages, cold emails, and 7-day follow-up sequences.
- **Target Audience:** HR Recruiters, Talent Acquisition Specialists, Business Development Managers, and Event Operations Leads at Bangalore MNCs.
- **Output:** Updates `e:\anti\Recruiter_Outreach_Messages.txt`.

---

### 4. `mnc_interview_coach`
- **Purpose:** Conducts realistic mock interviews and drills technical trade questions, behavioral STAR framework scenarios, and case studies.
- **Interview Topics:**
  - **Technical IB & Trade:** Incoterms 2020 (EXW, FOB, CIF, DDP), Customs Clearance, EXIM Docs, Letters of Credit, Forex Risk.
  - **Data & Analytics:** Advanced Excel (XLOOKUP, Pivot Tables), Power BI Dashboards, SQL basics.
  - **Behavioral (STAR):** Leading AERO India 2025 exhibition setup under tight timelines; resolving live soundcheck issues at TRILOGY; driving lead generation at Pencil Mark Interior.
