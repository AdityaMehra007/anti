const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const PREFS_JSON = path.join(CANDIDATE_DIR, 'candidate_search_preferences.json');
const REPORT_MD = path.join(WORKSPACE, 'Candidate_Search_Preferences_Report.md');

console.log("⚙️ Executing /setup --section search for Aditya Mehra...");

const searchPreferences = {
    framework_action: "/setup --section search",
    updated_at: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }),
    candidate: {
        name: "Aditya Mehra",
        degree: "BBA International Business, Dayananda Sagar University '26",
        verified_truth_base: [
            "300+ Event Deployments Managed (40+ corporate, 30+ live, 230+ pop-up)",
            "15% Operational Cost Savings via primary vendor negotiations",
            "INR 1.5L+ B2B Revenue Closed at Pencil Mark Interior Solutions",
            "Instawork AI Data Operations & ML Curation Mastery"
        ]
    },
    target_roles: [
        { title: "Global Business Operations Analyst", priority: "P1", fit_score: 9.8, target_salary_inr: "5.8L - 7.5L LPA" },
        { title: "Risk & Business Operations Advisory Analyst", priority: "P1", fit_score: 9.7, target_salary_inr: "6.0L - 8.0L LPA" },
        { title: "Business Development Executive", priority: "P1", fit_score: 9.9, target_salary_inr: "5.5L - 7.5L LPA" },
        { title: "EXIM & International Trade Associate", priority: "P2", fit_score: 9.5, target_salary_inr: "5.2L - 7.0L LPA" },
        { title: "AI Data Operations & Curation Specialist", priority: "P2", fit_score: 9.6, target_salary_inr: "6.0L - 8.5L LPA" }
    ],
    geographic_hubs: [
        { hub: "Bengaluru, India", tier: "PRIMARY_EXECUTION", focus_clusters: ["Outer Ring Road (Bellandur)", "Koramangala/HSR", "Whitefield", "Manyata", "CBD"] },
        { hub: "Dubai / UAE & Singapore", tier: "MID_TERM_TRANSFER", focus_clusters: ["EXIM Trade Ports", "Regional HQ Operations"] },
        { hub: "Global Remote", tier: "LONG_TERM", focus_clusters: ["US/EU Enterprise Software Ops"] }
    ],
    compensation_expectations: {
        minimum_acceptable_inr: "5,00,000 LPA",
        target_median_inr: "6,80,000 LPA",
        stretch_target_inr: "8,50,000 LPA",
        currency: "INR / USD"
    },
    preferred_working_modes: ["On-Site (Bangalore)", "Hybrid", "Global Remote"],
    target_employer_types: ["MNCs & GCCs (Accenture, Deloitte, EY, Amazon, GS)", "B2B SaaS Unicorns (HubSpot, Razorpay)", "EXIM Logistics (Freightify, Maersk)"]
};

fs.writeFileSync(PREFS_JSON, JSON.stringify(searchPreferences, null, 2), 'utf-8');

let reportMarkdown = `# ⚙️ /SETUP --SECTION SEARCH CONFIGURATION REPORT
**Candidate:** Aditya Mehra | BBA International Business, DSU Bangalore '26  
**Execution Timestamp:** ${searchPreferences.updated_at} IST  
**Framework Module:** MadsLorentzen/ai-job-search /setup Engine  

---

## 1. 🎯 Target Job Roles & Salary Bands

| Priority | Target Role Title | Fit Score | Target Salary Band (INR) | Primary Employers |
| :---: | :--- | :---: | :---: | :--- |
| **P1** | **Global Business Operations Analyst** | **9.8 / 10** | 5.8L - 7.5L LPA | Accenture India, Amazon |
| **P1** | **Risk & Business Operations Advisory Analyst** | **9.7 / 10** | 6.0L - 8.0L LPA | Deloitte US-India, EY GDS |
| **P1** | **Business Development Executive** | **9.9 / 10** | 5.5L - 7.5L LPA | Pencil Mark, HubSpot India |
| **P2** | **EXIM & International Trade Associate** | **9.5 / 10** | 5.2L - 7.0L LPA | Freightify, Maersk India |
| **P2** | **AI Data Operations & Curation Specialist** | **9.6 / 10** | 6.0L - 8.5L LPA | Instawork, AI Scale-Ups |

---

## 2. 📍 Geographic Hub & Work Mode Preferences

- **Primary Hub:** Bengaluru (Outer Ring Road, Koramangala, Whitefield, Manyata, CBD)
- **Mid-Term Expansion:** Dubai / UAE (0% Tax) & Singapore (Maritime EXIM)
- **Working Modes:** On-Site, Hybrid, Global Remote
- **Compensation Threshold:** Minimum INR 5.0L LPA | Target INR 6.8L - 8.5L LPA

---

## ⚡ Recommended System Action
Open **[index.html](file:///e:/anti/index.html)** to view configured search preferences integrated into the **61-JOB ACTIVE PIPELINE** tab.
`;

fs.writeFileSync(REPORT_MD, reportMarkdown, 'utf-8');
console.log(`✅ Candidate search preferences JSON written to: ${PREFS_JSON}`);
console.log(`✅ Search preferences report written to: ${REPORT_MD}`);
