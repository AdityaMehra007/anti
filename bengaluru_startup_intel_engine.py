"""
=============================================================================
BENGALURU STARTUP INTELLIGENCE ENGINE (BSIE-X)
-----------------------------------------------------------------------------
Autonomous intelligence engine, persistent SQLite database, daily change-log
delta tracker, ATS scoring analyzer, and REST API server for Bengaluru
startup career and business opportunities.

Tailored for: BBA International Business Freshers & Non-Sales Operations.
=============================================================================
"""

import sys
import os
import json
import sqlite3
import csv
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "bengaluru_startup_intel.sqlite")
SEED_PATH = os.path.join(DATA_DIR, "bengaluru_startup_intel.json")
DOSSIER_DIR = os.path.join(WORKSPACE_DIR, "applications_generated", "bengaluru_intel")

# Candidate DNA for deterministic scoring
CANDIDATE_PROFILE = {
    "name": "Adi",
    "degree": "BBA in International Business",
    "status": "Recent Graduate / Fresher",
    "key_skills": [
        "International Business", "Cross-Border Trade", "Global Sourcing",
        "Business Operations", "Strategic Market Research", "Executive Reporting",
        "Excel & Google Sheets", "Data Modeling", "Event Coordination",
        "Client Retention", "AI Workflow Automation", "Prompt Engineering"
    ],
    "negative_keywords": [
        "cold calling", "cold outreach", "sales quota", "field sales",
        "b2c telesales", "door-to-door", "lead gen commission", "sales development"
    ],
    "preferred_roles": [
        "Founder's Office", "Business Operations", "Sourcing & Logistics",
        "Strategy & Research", "Customer Success Operations", "Program Management"
    ]
}

def get_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Create relational schema and seed with verified data."""
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS startups (
        id TEXT PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        sector TEXT,
        stage TEXT,
        blr_location TEXT,
        website TEXT,
        founder TEXT,
        verified_active BOOLEAN DEFAULT 1
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,
        startup_name TEXT NOT NULL,
        role_title TEXT NOT NULL,
        category TEXT,
        fit_score INTEGER,
        work_mode TEXT,
        stipend_published TEXT,
        apply_url TEXT,
        experience_req TEXT,
        eligibility TEXT,
        posted_date TEXT,
        status TEXT DEFAULT 'Active',
        duties TEXT,
        why_it_fits TEXT,
        FOREIGN KEY (startup_name) REFERENCES startups(name)
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS funding_rounds (
        id TEXT PRIMARY KEY,
        entity_name TEXT NOT NULL,
        amount TEXT,
        round_type TEXT,
        announced_date TEXT,
        lead_investor TEXT,
        intended_use TEXT,
        public_rationale TEXT,
        source_url TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ecosystem_news (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT,
        date TEXT,
        summary TEXT,
        source_url TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS change_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        delta_id TEXT UNIQUE,
        status TEXT,
        record TEXT,
        finding TEXT,
        logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Seed data if present
    if os.path.exists(SEED_PATH):
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            seed = json.load(f)

        for s in seed.get("startups", []):
            c.execute("""
            INSERT OR REPLACE INTO startups (id, name, sector, stage, blr_location, website, founder, verified_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (s["id"], s["name"], s["sector"], s["stage"], s["blr_location"], s["website"], s["founder"], s["verified_active"]))

        for j in seed.get("jobs", []):
            c.execute("""
            INSERT OR REPLACE INTO jobs (id, startup_name, role_title, category, fit_score, work_mode, stipend_published, apply_url, experience_req, eligibility, posted_date, status, duties, why_it_fits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (j["id"], j["startup_name"], j["role_title"], j["category"], j["fit_score"], j["work_mode"], j["stipend_published"], j["apply_url"], j["experience_req"], j["eligibility"], j["posted_date"], j["status"], j["duties"], j["why_it_fits"]))

        for f_item in seed.get("funding", []):
            c.execute("""
            INSERT OR REPLACE INTO funding_rounds (id, entity_name, amount, round_type, announced_date, lead_investor, intended_use, public_rationale, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (f_item["id"], f_item["entity_name"], f_item["amount"], f_item["round_type"], f_item["announced_date"], f_item["lead_investor"], f_item["intended_use"], f_item["public_rationale"], f_item["source_url"]))

        for n in seed.get("news", []):
            c.execute("""
            INSERT OR REPLACE INTO ecosystem_news (id, title, category, date, summary, source_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (n["id"], n["title"], n["category"], n["date"], n["summary"], n["source_url"]))

        for d in seed.get("changelog", []):
            c.execute("""
            INSERT OR IGNORE INTO change_log (delta_id, status, record, finding)
            VALUES (?, ?, ?, ?)
            """, (d["delta_id"], d["status"], d["record"], d["finding"]))

        conn.commit()

    conn.close()
    print(f"Database initialized and seeded at {DB_PATH}")

def export_csvs():
    """Export all tables into dated and master CSV files."""
    conn = get_db()
    c = conn.cursor()

    tables = [
        ("jobs", os.path.join(DATA_DIR, "bengaluru_startup_jobs.csv")),
        ("funding_rounds", os.path.join(DATA_DIR, "bengaluru_startup_funding.csv")),
        ("ecosystem_news", os.path.join(DATA_DIR, "bengaluru_startup_news.csv")),
        ("change_log", os.path.join(DATA_DIR, "bengaluru_startup_daily_delta.csv")),
    ]

    for table_name, out_path in tables:
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        if rows:
            headers = [desc[0] for desc in c.description]
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for row in rows:
                    writer.writerow(list(row))
            print(f"Exported {len(rows)} rows to {out_path}")

    conn.close()

def calculate_fit_score(job_dict):
    """
    Deterministic role-fit score calculation (0 - 100) based on:
    - BBA Degree match (+25)
    - Non-Sales / Operational purity (+25)
    - Domain synergy (Sourcing / Strategy / BizOps / AI) (+20)
    - Compensation clarity (+15)
    - Location / Mode feasibility (+15)
    """
    score = 0
    reasons = []

    title = job_dict.get("role_title", "").lower()
    duties = job_dict.get("duties", "").lower()
    eligibility = job_dict.get("eligibility", "").lower()
    stipend = job_dict.get("stipend_published", "")

    # 1. Degree / Fresher eligibility
    if any(k in eligibility for k in ["bba", "business", "commerce", "fresher", "no experience"]):
        score += 25
        reasons.append("+25: Explicit BBA/fresher eligibility")
    elif "any graduate" in eligibility or "recent graduate" in eligibility:
        score += 20
        reasons.append("+20: Open graduate eligibility")
    else:
        score += 10

    # 2. Non-sales penalty/reward
    has_sales = any(k in duties or k in title for k in CANDIDATE_PROFILE["negative_keywords"])
    if not has_sales:
        score += 25
        reasons.append("+25: 100% pure operational/strategic mandate (No sales quotas)")
    else:
        score += 5
        reasons.append("+5: Contains customer acquisition / sales duties (penalty applied)")

    # 3. Domain synergy
    if any(k in title for k in ["founder", "operations", "strategy", "sourcing", "customer success", "program"]):
        score += 20
        reasons.append("+20: Core target track alignment")
    else:
        score += 10

    # 4. Compensation transparency
    if any(symbol in stipend for symbol in ["₹", "Rs", "Lakh", "$", "Paid"]):
        score += 15
        reasons.append("+15: Published transparent compensation")
    else:
        score += 5
        reasons.append("+5: Compensation undisclosed")

    # 5. Location / Work mode
    mode = job_dict.get("work_mode", "").lower()
    if "bengaluru" in mode or "remote" in mode or "in-office" in mode:
        score += 15
        reasons.append("+15: Prime Bengaluru or Remote mode")

    return min(100, score), reasons

def generate_daily_briefing():
    """Generates the structured daily briefing in Markdown format."""
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT * FROM jobs WHERE fit_score >= 90 ORDER BY fit_score DESC, id DESC LIMIT 5")
    top_jobs = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM funding_rounds ORDER BY id DESC LIMIT 3")
    funding = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM ecosystem_news ORDER BY id DESC LIMIT 3")
    news = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM change_log ORDER BY id DESC LIMIT 10")
    deltas = [dict(r) for r in c.fetchall()]

    conn.close()

    today = datetime.now().strftime("%A, %d %B %Y")

    lines = [
        f"# Bengaluru Startup Intelligence Briefing (Autonomous Dispatch)",
        f"**{today} | Curated for: Adi (BBA International Business Fresher - Operations Track)**",
        "",
        "## Executive Summary",
        f"- **Active Priority Pipeline:** {len(top_jobs)} tier-1 opportunities scored 90%+ fit for non-sales operations and founder's office.",
        "- **Capital Flow Momentum:** C-CAMP ₹500 Cr RDI commitment & Zen Technologies acquisition of Cogknit Semantics (₹135.15 Cr) leading ecosystem headlines.",
        "- **Immediate Action Mandate:** Submit tailored dossiers to Zethic Technologies (Founder's Office) and Y-Not (Emerging Talent Program).",
        "",
        "---",
        "",
        "## 1. Top Verified Job Opportunities (Ranked by Fit)",
        ""
    ]

    for j in top_jobs:
        lines.extend([
            f"### {j['id']} | {j['startup_name']}: {j['role_title']}",
            f"**Fit Score:** {j['fit_score']}/100 | **Work Mode:** {j['work_mode']} | **Compensation:** {j['stipend_published']}",
            f"**Application URL:** [{j['apply_url']}]({j['apply_url']})",
            f"**Experience Requirement:** {j['experience_req']}",
            f"**Core Responsibilities:** {j['duties']}",
            f"**Strategic Thesis:** {j['why_it_fits']}",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 2. Key Funding & M&A Developments",
        ""
    ])

    for f_item in funding:
        lines.extend([
            f"### {f_item['id']} | {f_item['entity_name']} — {f_item['amount']} ({f_item['round_type']})",
            f"- **Lead Investor:** {f_item['lead_investor']}",
            f"- **Capital Allocation:** {f_item['intended_use']}",
            f"- **Investment Rationale:** {f_item['public_rationale']}",
            f"- **Source Reference:** [{f_item['source_url']}]({f_item['source_url']})",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 3. Ecosystem & State Policy Signals",
        ""
    ])

    for n in news:
        lines.extend([
            f"### {n['id']} | {n['title']}",
            f"- **Category:** {n['category']} | **Date:** {n['date']}",
            f"- **Briefing:** {n['summary']}",
            f"- **Source:** [{n['source_url']}]({n['source_url']})",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## 4. Chronological Change Log & Daily Deltas",
        "",
        "| Delta ID | Status | Record | Key Finding |",
        "|---|---|---|---|"
    ])

    for d in deltas:
        lines.append(f"| {d['delta_id']} | `{d['status']}` | {d['record']} | {d['finding']} |")

    briefing_md = "\n".join(lines)
    briefing_path = os.path.join(DATA_DIR, f"daily_briefing_{datetime.now().strftime('%Y%m%d')}.md")
    with open(briefing_path, "w", encoding="utf-8") as f:
        f.write(briefing_md)

    print(f"Briefing written to {briefing_path}")
    return briefing_md

class IntelApiHandler(BaseHTTPRequestHandler):
    """REST API and Static Asset Handler for the Bengaluru Startup Intel Cockpit."""

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path in ["/", "/cockpit"]:
            cockpit_file = os.path.join(WORKSPACE_DIR, "bengaluru_startup_intelligence_cockpit.html")
            if not os.path.exists(cockpit_file):
                cockpit_file = os.path.join(WORKSPACE_DIR, "bengaluru_startup_cockpit.html")
            if os.path.exists(cockpit_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(cockpit_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Cockpit HTML not found")
            return

        if path.endswith(".html"):
            target_file = os.path.join(WORKSPACE_DIR, os.path.basename(path))
            if os.path.exists(target_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(target_file, "rb") as f:
                    self.wfile.write(f.read())
                return

        conn = get_db()
        c = conn.cursor()

        if path == "/api/stats":
            c.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 90")
            high_fit_jobs = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM funding_rounds")
            total_funding = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM ecosystem_news")
            total_news = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM change_log")
            total_deltas = c.fetchone()[0]

            self._send_json({
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "total_jobs": total_jobs,
                    "high_fit_jobs": high_fit_jobs,
                    "total_funding_deals": total_funding,
                    "total_ecosystem_events": total_news,
                    "active_deltas": total_deltas
                },
                "target_candidate": CANDIDATE_PROFILE
            })

        elif path == "/api/jobs":
            query = "SELECT * FROM jobs WHERE 1=1"
            args = []

            if "fit" in params:
                query += " AND fit_score >= ?"
                args.append(int(params["fit"][0]))

            if "mode" in params:
                query += " AND work_mode LIKE ?"
                args.append(f"%{params['mode'][0]}%")

            if "category" in params:
                query += " AND category LIKE ?"
                args.append(f"%{params['category'][0]}%")

            query += " ORDER BY fit_score DESC, id DESC"
            c.execute(query, args)
            jobs = [dict(r) for r in c.fetchall()]
            self._send_json({"count": len(jobs), "jobs": jobs})

        elif path.startswith("/api/jobs/"):
            job_id = path.replace("/api/jobs/", "").strip()
            c.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
            row = c.fetchone()
            if row:
                self._send_json({"status": "found", "job": dict(row)})
            else:
                self._send_json({"error": "Job not found"}, status=404)

        elif path == "/api/funding":
            c.execute("SELECT * FROM funding_rounds ORDER BY id DESC")
            funding = [dict(r) for r in c.fetchall()]
            self._send_json({"count": len(funding), "funding": funding})

        elif path == "/api/news":
            c.execute("SELECT * FROM ecosystem_news ORDER BY id DESC")
            news = [dict(r) for r in c.fetchall()]
            self._send_json({"count": len(news), "news": news})

        elif path == "/api/changelog":
            c.execute("SELECT * FROM change_log ORDER BY id DESC")
            deltas = [dict(r) for r in c.fetchall()]
            self._send_json({"count": len(deltas), "changelog": deltas})

        elif path == "/api/dossiers":
            dossiers = []
            if os.path.exists(DOSSIER_DIR):
                for fname in sorted(os.listdir(DOSSIER_DIR)):
                    if fname.endswith(".md"):
                        dpath = os.path.join(DOSSIER_DIR, fname)
                        with open(dpath, "r", encoding="utf-8") as df:
                            content = df.read()
                        dossiers.append({
                            "filename": fname,
                            "title": fname.replace(".md", "").replace("_", " "),
                            "content": content
                        })
            self._send_json({"count": len(dossiers), "dossiers": dossiers})

        else:
            self._send_json({"error": "Endpoint not recognized"}, status=404)

        conn.close()

def run_server(port=8792):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, IntelApiHandler)
    print(f"[*] Bengaluru Startup Intelligence API Server live on http://127.0.0.1:{port}")
    print(f"[*] Interactive Cockpit available at http://127.0.0.1:{port}/cockpit")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server gracefully.")
        httpd.server_close()

if __name__ == "__main__":
    # Ensure stdout handles UTF-8 on Windows
    if sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    if "--init-db" in sys.argv:
        init_database()
    elif "--export" in sys.argv:
        init_database()
        export_csvs()
    elif "--briefing" in sys.argv:
        init_database()
        briefing_text = generate_daily_briefing()
        try:
            print(briefing_text)
        except UnicodeEncodeError:
            print(briefing_text.encode("ascii", errors="replace").decode("ascii"))
    elif "--serve" in sys.argv:
        init_database()
        export_csvs()
        port = 8792
        if len(sys.argv) > 2 and sys.argv[sys.argv.index("--serve") + 1].isdigit():
            port = int(sys.argv[sys.argv.index("--serve") + 1])
        run_server(port)
    else:
        init_database()
        export_csvs()
        print("Usage: python bengaluru_startup_intel_engine.py [--init-db | --export | --briefing | --serve [port]]")
