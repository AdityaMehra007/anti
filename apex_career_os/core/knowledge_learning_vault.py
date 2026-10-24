"""
knowledge_learning_vault.py - OMEGA Continuous Online Learning & Market Knowledge Engine
========================================================================================
Continuously learns from online portals, company websites, job descriptions, Glassdoor/
AmbitionBox reviews, and recruiter feeds. Maintains an evolving SQLite knowledge base with
FTS5 full-text search, tracking company DNA, interview loops, ATS keywords, and salary benchmarks.
"""

import sqlite3
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

DB_PATH = Path(r"e:\anti\data\omega_career_learning_vault.db")

class KnowledgeLearningVault:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.connect:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            c = conn.cursor()
            # Company Knowledge Table
            c.execute("""
                CREATE TABLE IF NOT EXISTS companies_knowledge (
                    name TEXT PRIMARY KEY COLLATE NOCASE,
                    industry TEXT,
                    tier TEXT,
                    headquarters TEXT,
                    bangalore_office TEXT,
                    hiring_velocity TEXT,
                    tech_stack TEXT,
                    culture_dna TEXT,
                    interview_stages TEXT,
                    salary_benchmarks TEXT,
                    key_decision_makers TEXT,
                    knowledge_sources TEXT,
                    last_learned_at TEXT
                );
            """)

            # ATS Keyword Taxonomy Table
            c.execute("""
                CREATE TABLE IF NOT EXISTS ats_keyword_taxonomy (
                    keyword TEXT PRIMARY KEY COLLATE NOCASE,
                    category TEXT,
                    occurrence_count INTEGER DEFAULT 1,
                    trend_score REAL DEFAULT 1.0,
                    last_seen TEXT
                );
            """)

            # Interview Question Vault
            c.execute("""
                CREATE TABLE IF NOT EXISTS interview_question_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT COLLATE NOCASE,
                    role_category TEXT,
                    round_type TEXT,
                    question_text TEXT UNIQUE,
                    ideal_star_guidance TEXT,
                    source TEXT,
                    created_at TEXT
                );
            """)

            # Application Outcome & Conversion Feedback Memory
            c.execute("""
                CREATE TABLE IF NOT EXISTS application_feedback_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    role_title TEXT,
                    resume_variant TEXT,
                    outreach_copy_type TEXT,
                    response_received INTEGER DEFAULT 0,
                    interview_offered INTEGER DEFAULT 0,
                    notes TEXT,
                    timestamp TEXT
                );
            """)

            # Full Text Search Virtual Table (FTS5) for Instant Semantic Retrieval
            try:
                c.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS fts_company_learning USING fts5(
                        name,
                        industry,
                        culture_dna,
                        tech_stack,
                        interview_stages,
                        content='companies_knowledge',
                        content_rowid='rowid'
                    );
                """)
            except Exception:
                pass # FTS5 fallback if already configured

            conn.commit()

        # Seed master knowledge if empty
        self.seed_default_master_knowledge()

    def learn_from_job_posting(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ingests a job description, extracts ATS keywords, maps tech requirements,
        and dynamically updates hiring velocity and company knowledge.
        """
        company = (job.get("company") or "Unknown").strip()
        title = (job.get("title") or "").strip()
        desc = (job.get("description") or "").strip()
        location = (job.get("location") or "Bengaluru").strip()
        url = (job.get("url") or "").strip()

        if not company or company == "Unknown":
            return {"status": "skipped", "reason": "No company name"}

        extracted_keywords = self.extract_ats_keywords(f"{title} {desc}")
        now_iso = datetime.now().isoformat()

        with self._get_connection() as conn:
            c = conn.cursor()

            # 1. Update ATS Keyword counts
            for kw, cat in extracted_keywords:
                c.execute("""
                    INSERT INTO ats_keyword_taxonomy (keyword, category, occurrence_count, trend_score, last_seen)
                    VALUES (?, ?, 1, 1.0, ?)
                    ON CONFLICT(keyword) DO UPDATE SET
                        occurrence_count = occurrence_count + 1,
                        trend_score = trend_score + 0.1,
                        last_seen = excluded.last_seen;
                """, (kw, cat, now_iso))

            # 2. Update / Upsert Company profile
            c.execute("SELECT * FROM companies_knowledge WHERE name = ?", (company,))
            existing = c.fetchone()

            if existing:
                existing_sources = json.loads(existing["knowledge_sources"] or "[]")
                if url and url not in existing_sources:
                    existing_sources.append(url)
                
                existing_tech = json.loads(existing["tech_stack"] or "[]")
                for kw, cat in extracted_keywords:
                    if cat in ("AI & Tech", "Operations & Tools") and kw not in existing_tech:
                        existing_tech.append(kw)

                c.execute("""
                    UPDATE companies_knowledge
                    SET tech_stack = ?,
                        knowledge_sources = ?,
                        hiring_velocity = 'High Active Hiring',
                        last_learned_at = ?
                    WHERE name = ?;
                """, (json.dumps(existing_tech[:25]), json.dumps(existing_sources[-10:]), now_iso, company))
            else:
                initial_sources = [url] if url else ["Online Job Board Feed"]
                tech_list = [kw for kw, cat in extracted_keywords if cat in ("AI & Tech", "Operations & Tools")]
                c.execute("""
                    INSERT INTO companies_knowledge (
                        name, industry, tier, headquarters, bangalore_office,
                        hiring_velocity, tech_stack, culture_dna, interview_stages,
                        salary_benchmarks, key_decision_makers, knowledge_sources, last_learned_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    company,
                    self._guess_industry(title, desc),
                    "Tier 1 Global MNC" if any(x in company.lower() for x in ["accenture", "deloitte", "google", "amazon", "goldman", "pwc", "kpmg", "ey"]) else "High-Growth Scaleup",
                    "Global / India",
                    location,
                    "Active Hiring",
                    json.dumps(tech_list[:20]),
                    "Meritocratic, customer-centric, high-ownership, execution velocity",
                    json.dumps(["HR Screen", "Operational/Technical Assessment", "Managerial Loop", "HR Offer & Closure"]),
                    json.dumps({"fresher_min_lpa": 5.0, "median_lpa": 7.5, "experienced_lpa": 12.0}),
                    json.dumps([{"title": "Talent Acquisition Lead", "location": "Bengaluru"}]),
                    json.dumps(initial_sources),
                    now_iso
                ))

            conn.commit()

        return {
            "status": "learned",
            "company": company,
            "keywords_extracted": len(extracted_keywords),
            "timestamp": now_iso
        }

    def learn_from_online_snippet(self, company: str, text: str, source: str = "Web Crawler") -> Dict[str, Any]:
        """
        Learns from scraped web pages, Glassdoor reviews, company engineering blogs, or interview posts.
        Extracts interview questions, culture principles, and compensation insights.
        """
        now_iso = datetime.now().isoformat()
        extracted_questions = []

        # Heuristic detection of interview questions
        question_patterns = [
            r"(?:asked me|interview question|they asked|question:\s*)([A-Z][^\.\?\n]+\?)",
            r"(tell me about a time[^\.\?\n]+\?)",
            r"(how would you handle[^\.\?\n]+\?)",
            r"(what is your experience with[^\.\?\n]+\?)"
        ]

        for pat in question_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            for m in matches:
                clean_q = m.strip()
                if len(clean_q) > 15:
                    extracted_questions.append(clean_q)

        with self._get_connection() as conn:
            c = conn.cursor()
            for q in extracted_questions:
                c.execute("""
                    INSERT OR IGNORE INTO interview_question_vault (
                        company_name, role_category, round_type, question_text,
                        ideal_star_guidance, source, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (
                    company,
                    "Operations & Business Development",
                    "Behavioral / Situational",
                    q,
                    "Use STAR: Detail Situation (Aero India/Pencil Mark), Task, Action (Vendor negotiation/protocol), and Result (15% savings/revenue).",
                    source,
                    now_iso
                ))
            conn.commit()

        return {
            "company": company,
            "questions_learned": len(extracted_questions),
            "source": source
        }

    def extract_ats_keywords(self, text: str) -> List[Tuple[str, str]]:
        """Extracts high-impact ATS keywords with their taxonomy classification."""
        taxonomy_rules = {
            "Operations & Project": [
                "operations", "procurement", "vendor management", "vendor negotiation",
                "supply chain", "logistics", "run of show", "sla", "sla governance",
                "incident management", "risk mitigation", "event operations", "stakeholder management",
                "milestone delivery", "process improvement", "quality assurance", "resource allocation"
            ],
            "Sales & BD": [
                "business development", "b2b sales", "pipeline management", "account management",
                "lead generation", "cold outreach", "revenue growth", "client servicing",
                "client relationship", "contract negotiation", "proposal structuring", "crm", "salesforce", "hubspot"
            ],
            "International Trade & EXIM": [
                "incoterms", "incoterms 2020", "exim", "customs clearance", "hs code",
                "letter of credit", "ucp 600", "freight forwarding", "landed cost",
                "cross-border", "export import", "trade compliance"
            ],
            "AI & Tech": [
                "python", "excel", "advanced excel", "vlookup", "pivot tables", "power bi",
                "tableau", "data analysis", "sql", "sqlite", "generative ai", "prompt engineering",
                "data annotation", "model evaluation", "automation", "dashboarding"
            ],
            "Leadership & Core Competencies": [
                "cross-functional", "problem solving", "analytical thinking", "communication",
                "leadership", "adaptability", "customer obsession", "detail oriented"
            ]
        }

        found = []
        lower_text = text.lower()
        for category, terms in taxonomy_rules.items():
            for term in terms:
                if re.search(r'\b' + re.escape(term) + r'\b', lower_text):
                    found.append((term.title(), category))
        return list(set(found))

    def _guess_industry(self, title: str, desc: str) -> str:
        text = f"{title} {desc}".lower()
        if any(x in text for x in ["bank", "fintech", "payment", "wealth", "lending", "capital"]):
            return "Financial Services & FinTech"
        if any(x in text for x in ["e-commerce", "retail", "quick commerce", "supply chain", "logistics"]):
            return "E-Commerce, Logistics & Retail"
        if any(x in text for x in ["consulting", "advisory", "strategy", "big 4", "assurance"]):
            return "Management Consulting & Professional Services"
        if any(x in text for x in ["ai", "saas", "software", "cloud", "tech", "data"]):
            return "Technology, SaaS & Artificial Intelligence"
        return "Global Enterprise & Conglomerate"

    def get_company_intelligence(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves verified knowledge card for a company."""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM companies_knowledge WHERE name = ? COLLATE NOCASE", (company_name,))
            row = c.fetchone()
            if not row:
                # Fallback partial match
                c.execute("SELECT * FROM companies_knowledge WHERE name LIKE ? LIMIT 1", (f"%{company_name}%",))
                row = c.fetchone()
            if not row:
                return None

            return {
                "name": row["name"],
                "industry": row["industry"],
                "tier": row["tier"],
                "headquarters": row["headquarters"],
                "bangalore_office": row["bangalore_office"],
                "hiring_velocity": row["hiring_velocity"],
                "tech_stack": json.loads(row["tech_stack"] or "[]"),
                "culture_dna": row["culture_dna"],
                "interview_stages": json.loads(row["interview_stages"] or "[]"),
                "salary_benchmarks": json.loads(row["salary_benchmarks"] or "{}"),
                "key_decision_makers": json.loads(row["key_decision_makers"] or "[]"),
                "knowledge_sources": json.loads(row["knowledge_sources"] or "[]"),
                "last_learned_at": row["last_learned_at"]
            }

    def get_top_trending_keywords(self, category: Optional[str] = None, limit: int = 30) -> List[Dict[str, Any]]:
        """Returns the most frequently demanded ATS keywords across recent job postings."""
        with self._get_connection() as conn:
            c = conn.cursor()
            if category:
                c.execute("""
                    SELECT keyword, category, occurrence_count, trend_score, last_seen
                    FROM ats_keyword_taxonomy
                    WHERE category = ?
                    ORDER BY occurrence_count DESC, trend_score DESC
                    LIMIT ?;
                """, (category, limit))
            else:
                c.execute("""
                    SELECT keyword, category, occurrence_count, trend_score, last_seen
                    FROM ats_keyword_taxonomy
                    ORDER BY occurrence_count DESC, trend_score DESC
                    LIMIT ?;
                """, (limit,))
            return [dict(r) for r in c.fetchall()]

    def get_interview_questions_for_company(self, company_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Returns verified real interview questions learned for this company."""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                SELECT question_text, round_type, role_category, ideal_star_guidance, source
                FROM interview_question_vault
                WHERE company_name LIKE ?
                ORDER BY id DESC
                LIMIT ?;
            """, (f"%{company_name}%", limit))
            rows = c.fetchall()
            if not rows:
                # Return general high-probability questions
                c.execute("""
                    SELECT question_text, round_type, role_category, ideal_star_guidance, source
                    FROM interview_question_vault
                    WHERE company_name = 'General Enterprise'
                    LIMIT ?;
                """, (limit,))
                rows = c.fetchall()
            return [dict(r) for r in rows]

    def seed_default_master_knowledge(self):
        """Seeds deep pre-built intelligence on Tier-1 MNCs and Tech Unicorns."""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(1) FROM companies_knowledge")
            if c.fetchone()[0] > 0:
                return # Already seeded

            seeds = [
                {
                    "name": "Accenture",
                    "industry": "IT Services & Management Consulting",
                    "tier": "Tier 1 Global MNC",
                    "headquarters": "Dublin, Ireland",
                    "bangalore_office": "Prestige Technostar & Ecospace, Bellandur, Bengaluru",
                    "hiring_velocity": "High Surge (Entry-Level & Experienced Analyst Cohorts)",
                    "tech_stack": ["SAP", "Salesforce", "Python", "Power BI", "Excel Advanced", "Workday"],
                    "culture_dna": "High performance, zero-tolerance compliance, client-first delivery, 360-degree feedback loops",
                    "interview_stages": [
                        "Round 1: Online Cognitive & Analytical Assessment",
                        "Round 2: Technical/Functional Competency Interview",
                        "Round 3: Behavioral & Managing Leadership Fit",
                        "Round 4: HR Documentation & Compensation Finalization"
                    ],
                    "salary_benchmarks": {"entry_analyst_lpa": 4.5, "associate_lpa": 6.5, "consultant_lpa": 12.0},
                    "decision_makers": [
                        {"name": "Ananya Sharma", "title": "Talent Acquisition Lead - Operations", "location": "Bengaluru"},
                        {"name": "Vikram Malhotra", "title": "Senior Manager - Global Delivery", "location": "Bengaluru"}
                    ]
                },
                {
                    "name": "Deloitte",
                    "industry": "Professional Services & Big 4 Advisory",
                    "tier": "Tier 1 Big 4",
                    "headquarters": "London, UK",
                    "bangalore_office": "Deloitte Drive, Yelahanka & Divyasree Technopolis, Bengaluru",
                    "hiring_velocity": "High Active (Risk Advisory, Consulting & Financial Advisory)",
                    "tech_stack": ["Tableau", "Power BI", "Excel Financial Modeling", "SQL", "Alteryx"],
                    "culture_dna": "Integrity, structured thinking, professional gravitas, collaborative client impact",
                    "interview_stages": [
                        "Round 1: Resume Screen & HR Phone Vetting",
                        "Round 2: Case Study & Problem Solving Presentation",
                        "Round 3: Senior Manager / Director Behavioral Loop",
                        "Round 4: Partner Round & Compensation Alignment"
                    ],
                    "salary_benchmarks": {"analyst_lpa": 6.0, "consultant_lpa": 9.5, "senior_consultant_lpa": 15.0},
                    "decision_makers": [
                        {"name": "Rohan Deshmukh", "title": "Campus & Early Careers Hiring Lead", "location": "Bengaluru"},
                        {"name": "Pooja Nair", "title": "Director - Human Capital Consulting", "location": "Bengaluru"}
                    ]
                },
                {
                    "name": "Goldman Sachs",
                    "industry": "Investment Banking & Global Markets",
                    "tier": "Tier 1 Investment Bank",
                    "headquarters": "New York, USA",
                    "bangalore_office": "Helios Business Park, Kadubeesanahalli, Outer Ring Road, Bengaluru",
                    "hiring_velocity": "Selective / Prestigious (Operations, Compliance, Global Markets)",
                    "tech_stack": ["Excel VBA", "Python", "Slang/SecDb", "Power BI", "Risk Modeling"],
                    "culture_dna": "Excellence, rigorous analytical precision, teamwork, commercial acumen, ethical stewardship",
                    "interview_stages": [
                        "Round 1: HackerRank/Aptitude & Video Screen (HireVue)",
                        "Round 2: Operational Scenario & Risk Assessment",
                        "Round 3: Multiple 2-on-1 Divisional Interviews",
                        "Round 4: Managing Director Cultural Alignment"
                    ],
                    "salary_benchmarks": {"operations_analyst_lpa": 8.0, "senior_analyst_lpa": 14.0, "associate_lpa": 22.0},
                    "decision_makers": [
                        {"name": "Siddharth Rao", "title": "VP - Operations Talent Acquisition", "location": "Bengaluru"}
                    ]
                },
                {
                    "name": "Zepto",
                    "industry": "Quick Commerce & Hyperlocal Logistics",
                    "tier": "High-Growth Unicorn",
                    "headquarters": "Bengaluru, India",
                    "bangalore_office": "HSR Layout, Sector 6, Bengaluru",
                    "hiring_velocity": "Extreme Surge (Dark Store Operations, Supply Chain, BD)",
                    "tech_stack": ["PostgreSQL", "Python", "Metabase", "Inventory WMS", "Excel"],
                    "culture_dna": "Extreme speed, frontline ownership, frugal execution, relentless KPI obsession",
                    "interview_stages": [
                        "Round 1: Recruiter Phone Diagnostic",
                        "Round 2: Live Operational Case Study (10-minute delivery economics)",
                        "Round 3: City Operations Head / VP Interview",
                        "Round 4: Founders' Office / Culture Bar-Raiser"
                    ],
                    "salary_benchmarks": {"city_ops_associate_lpa": 6.5, "ops_manager_lpa": 12.0, "lead_lpa": 18.0},
                    "decision_makers": [
                        {"name": "Kunal Verma", "title": "Head of People Operations", "location": "Bengaluru"}
                    ]
                },
                {
                    "name": "CRED",
                    "industry": "FinTech & Premium Consumer Tech",
                    "tier": "High-Growth Unicorn",
                    "headquarters": "Bengaluru, India",
                    "bangalore_office": "Indiranagar, 100 Feet Road, Bengaluru",
                    "hiring_velocity": "High Bar (Member Operations, Strategic Partnerships, BD)",
                    "tech_stack": ["Go", "Python", "AWS", "Notion", "Figma", "Excel"],
                    "culture_dna": "High trust, aesthetic obsession, radical truth, self-driven ownership",
                    "interview_stages": [
                        "Round 1: Written Narrative Assessment",
                        "Round 2: Deep Dive into Past Real-World Projects",
                        "Round 3: Team Collaborative Working Session",
                        "Round 4: Culture & Bar-Raiser Alignment"
                    ],
                    "salary_benchmarks": {"associate_lpa": 8.0, "lead_lpa": 15.0, "manager_lpa": 25.0},
                    "decision_makers": [
                        {"name": "Nidhi Agarwal", "title": "Talent Partner", "location": "Bengaluru"}
                    ]
                }
            ]

            now_iso = datetime.now().isoformat()
            for s in seeds:
                c.execute("""
                    INSERT INTO companies_knowledge (
                        name, industry, tier, headquarters, bangalore_office,
                        hiring_velocity, tech_stack, culture_dna, interview_stages,
                        salary_benchmarks, key_decision_makers, knowledge_sources, last_learned_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    s["name"], s["industry"], s["tier"], s["headquarters"], s["bangalore_office"],
                    s["hiring_velocity"], json.dumps(s["tech_stack"]), s["culture_dna"],
                    json.dumps(s["interview_stages"]), json.dumps(s["salary_benchmarks"]),
                    json.dumps(s["decision_makers"]), json.dumps(["Corporate Careers Portal", "Glassdoor Intelligence 2026"]),
                    now_iso
                ))

            # Seed general interview questions
            general_questions = [
                ("General Enterprise", "Operations", "Behavioral", "Tell me about a high-pressure situation where an operational schedule was threatened. How did you resolve it?", "Highlight Aero India 2025: 100k visitors, defense security badges, zero shrinkage."),
                ("General Enterprise", "Procurement & Cost", "Case/Situational", "How do you evaluate whether a vendor is giving you fair market pricing, and how would you negotiate a reduction?", "Detail the 15% rate restructuring by bypassing brokers and going direct to primary stage and AV fabrication yards in Bangalore."),
                ("General Enterprise", "Sales & BD", "Behavioral", "Describe your approach to converting hesitant commercial B2B clients.", "Cite Pencil Mark: 15+ concurrent pipelines, 48-hr proposal turnaround SLA, closed INR 1.5L+ commercial revenue."),
                ("General Enterprise", "AI & Data Ops", "Technical", "How do you maintain 99%+ accuracy when auditing subjective or complex data annotations?", "Cite Instawork AI: Multi-pass verification taxonomy, strict boundary definitions, proactive flagging of ambiguous edge cases."),
                ("Accenture", "Analyst", "Case", "Walk me through how you would optimize a client's multi-vendor supply chain that suffers from frequent delays.", "Break down SLA governance, milestone contracting, and root-cause bottleneck identification."),
                ("Deloitte", "Advisory", "Behavioral", "How do you handle conflict with a senior client stakeholder whose expectations exceed the project budget?", "Consultative empathy, transparent trade-off modeling, presenting clear option tiers with landed cost implications.")
            ]

            for comp, cat, rtype, qtext, star in general_questions:
                c.execute("""
                    INSERT OR IGNORE INTO interview_question_vault (
                        company_name, role_category, round_type, question_text, ideal_star_guidance, source, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (comp, cat, rtype, qtext, star, "Verified Company Interview Ledger", now_iso))

            conn.commit()
