const fs = require('fs');
const path = require('path');

const WORKSPACE = 'e:/anti';
const CANDIDATE_DIR = path.join(WORKSPACE, 'career-hub', 'candidate');
const DB_JSON = path.join(CANDIDATE_DIR, 'career_empire_master_data.json');

console.log("🗄️ Initializing ANTIGRAVITY CAREER EMPIRE OS 22-Table Data Engine...");

const dbSchema = {
    system_version: "CAREER_EMPIRE_OS_V19",
    initialized_at: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" }),
    single_source_of_truth: {
        candidate_id: "CAND-001",
        full_legal_name: "Aditya Mehra",
        preferred_name: "Aditya",
        current_city: "Bengaluru, Karnataka, India",
        target_cities: ["Bengaluru", "Dubai / UAE", "Singapore", "Global Remote"],
        relocation_willingness: true,
        remote_preference: "Hybrid / Remote-First",
        degree: "BBA International Business",
        university: "Dayananda Sagar University",
        graduation_status: "Pursuing (Class of 2026)",
        graduation_date: "June 2026",
        verified_evidence: [
            { id: "EVID-001", claim: "300+ Event Deployments Managed", metrics: "40+ corporate, 30+ live, 230+ pop-up; 15% net cost savings via direct vendor rate cards", confidence: "VERIFIED" },
            { id: "EVID-002", claim: "INR 1.5L+ B2B Closed Revenue", metrics: "Pencil Mark Interior Solutions, 15+ corporate client accounts managed", confidence: "VERIFIED" },
            { id: "EVID-003", claim: "Instawork AI Data Operations", metrics: "Structured ML workflow curation, quality auditing, 3.2x throughput increase", confidence: "VERIFIED" },
            { id: "EVID-004", claim: "EXIM Trade & Incoterms 2020 Compliance", metrics: "BBA IB formal curriculum, FOB/CIF landed cost modeling, customs documentation", confidence: "VERIFIED" }
        ]
    },
    tables: {
        candidates: [{ id: "CAND-001", name: "Aditya Mehra", status: "ACTIVE" }],
        companies: [],
        contacts: [],
        roles: [],
        skills: [
            { skill: "Global Business Operations", category: "business", confidence: "VERIFIED" },
            { skill: "B2B Outbound Sales", category: "commercial", confidence: "VERIFIED" },
            { skill: "Vendor Management & Rate Card Negotiation", category: "operations", confidence: "VERIFIED" },
            { skill: "EXIM Incoterms 2020 Compliance", category: "domain knowledge", confidence: "VERIFIED" },
            { skill: "AI Data Operations & ML Curation", category: "AI / digital", confidence: "VERIFIED" }
        ],
        applications: [],
        interviews: [],
        offers: [],
        outreach: [],
        followups: [],
        projects: [],
        certifications: [],
        education: [],
        experiences: [],
        hiring_signals: [],
        company_events: [],
        job_sources: [],
        market_segments: [],
        outcomes: [],
        experiments: [],
        system_tasks: [],
        audit_log: [
            { timestamp: new Date().toISOString(), event: "22-Table Database Schema Initialized", status: "SUCCESS" }
        ]
    }
};

fs.writeFileSync(DB_JSON, JSON.stringify(dbSchema, null, 2), 'utf-8');
console.log(`✅ 22-Table Master Database JSON written to: ${DB_JSON}`);
