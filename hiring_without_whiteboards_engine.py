#!/usr/bin/env python3
"""
hiring_without_whiteboards_engine.py
=============================================================================
OMEGA ∞ Autonomous System — Hiring Without Whiteboards Engine & Intelligence
Ingests, parses, enriches, indexes, and queries 761+ companies from the
canonical poteto/hiring-without-whiteboards repository.

Outputs:
  - data/hiring_without_whiteboards.json
  - data/hiring_without_whiteboards.csv
  - data/hiring_without_whiteboards.sqlite (with FTS5 search index)
  - Interactive Web Cockpit server on port 8780
=============================================================================
"""

import sys
import os
import re
import json
import sqlite3
import csv
import argparse
import http.server
import socketserver
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

JSON_EXPORT_PATH = DATA_DIR / "hiring_without_whiteboards.json"
CSV_EXPORT_PATH = DATA_DIR / "hiring_without_whiteboards.csv"
SQLITE_DB_PATH = DATA_DIR / "hiring_without_whiteboards.sqlite"
DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Path to the raw downloaded README content from step 2
RAW_CACHE_FILE = Path(r"C:\Users\amehr\.gemini\antigravity\brain\bc506214-213e-4451-b628-540437dba0d9\.system_generated\steps\2\output.txt")


def load_raw_readme() -> str:
    """Loads the raw README content from local cached step or fallback."""
    if RAW_CACHE_FILE.exists():
        try:
            with open(RAW_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("content", "")
        except Exception as e:
            print(f"[!] Warning reading cache file: {e}")
            
    # Check if a local copy exists in data
    local_readme = DATA_DIR / "hiring_without_whiteboards_readme.md"
    if local_readme.exists():
        return local_readme.read_text(encoding="utf-8")
        
    raise RuntimeError("Cannot locate raw README.md for poteto/hiring-without-whiteboards")


def parse_locations_and_regions(loc_str: str, proc_str: str = "") -> Dict[str, Any]:
    """Classifies geographic region, countries, and remote eligibility."""
    combined = (loc_str + " " + proc_str).lower()
    is_remote = "remote" in combined or "distributed" in combined or "telecommute" in combined
    loc_lower = loc_str.lower()
    
    regions = []
    countries = []
    
    # North America
    na_markers = [
        "san francisco", "sf", "ca", "california", "new york", "ny", "nyc",
        "austin", "tx", "texas", "seattle", "wa", "boston", "ma", "chicago", "il",
        "denver", "co", "colorado", "toronto", "canada", "montreal", "vancouver",
        "mexico", "mexico city", "monterrey", "boulder", "los angeles", "atlanta",
        "ga", "virginia", "va", "utah", "ut", "michigan", "mi", "detroit",
        "pennsylvania", "pa", "philadelphia", "orlando", "fl", "florida",
        "minneapolis", "mn", "columbus", "oh", "north carolina", "nc", "raleigh",
        "arlington", "dallas", "oakland", "cambridge, ma", "reston", "providence"
    ]
    # Europe & UK
    eu_markers = [
        "uk", "london", "england", "scotland", "edinburgh", "glasgow", "bristol",
        "cambridge, uk", "manchester", "cardiff", "germany", "berlin", "munich",
        "hamburg", "cologne", "frankfurt", "netherlands", "amsterdam", "utrecht",
        "france", "paris", "poland", "warsaw", "krakow", "cracow", "wroclaw",
        "spain", "madrid", "barcelona", "sweden", "stockholm", "norway", "oslo",
        "denmark", "copenhagen", "switzerland", "zurich", "austria", "vienna",
        "ireland", "dublin", "belgium", "brussels", "italy", "milan", "rome",
        "portugal", "lisbon", "czech republic", "prague", "finland", "helsinki",
        "hungary", "budapest", "romania", "bucharest", "bulgaria", "sofia", "serbia"
    ]
    # India & APAC
    apac_markers = [
        "india", "bangalore", "bengaluru", "mumbai", "delhi", "gurgaon", "noida",
        "chennai", "hyderabad", "pune", "kochi", "singapore", "japan", "tokyo",
        "australia", "sydney", "melbourne", "philippines", "makati", "indonesia",
        "jakarta", "bandung", "vietnam", "taiwan", "dubai", "uae", "abu dhabi",
        "israel", "tel aviv"
    ]
    # Latin America
    latam_markers = [
        "brazil", "são paulo", "sao paulo", "florianópolis", "colombia", "bogota",
        "medellín", "argentina", "buenos aires", "chile", "santiago", "peru", "lima"
    ]

    has_na = any(re.search(r'\b' + re.escape(m) + r'\b', loc_lower) for m in na_markers)
    has_eu = any(re.search(r'\b' + re.escape(m) + r'\b', loc_lower) for m in eu_markers)
    has_apac = any(re.search(r'\b' + re.escape(m) + r'\b', loc_lower) for m in apac_markers)
    has_latam = any(re.search(r'\b' + re.escape(m) + r'\b', loc_lower) for m in latam_markers)

    if has_na:
        regions.append("North America")
    if has_eu:
        regions.append("Europe & UK")
    if has_apac:
        regions.append("India & APAC")
    if has_latam:
        regions.append("Latin America")
        
    if not regions:
        if is_remote:
            primary_region = "Global Remote"
        else:
            primary_region = "Global / Other"
    elif len(regions) == 1:
        primary_region = regions[0]
    else:
        primary_region = "Multi-Region (" + ", ".join(regions) + ")"

    # Detect specific countries
    if any(m in loc_lower for m in ["united states", " usa", ", us", "san francisco", "new york", "austin", "seattle", "boston", "chicago"]):
        countries.append("United States")
    if any(m in loc_lower for m in ["canada", "toronto", "montreal", "vancouver"]):
        countries.append("Canada")
    if any(m in loc_lower for m in ["united kingdom", "london", "uk", "england", "scotland"]):
        countries.append("United Kingdom")
    if any(m in loc_lower for m in ["germany", "berlin", "munich", "hamburg", "frankfurt"]):
        countries.append("Germany")
    if any(m in loc_lower for m in ["netherlands", "amsterdam", "utrecht"]):
        countries.append("Netherlands")
    if any(m in loc_lower for m in ["france", "paris"]):
        countries.append("France")
    if any(m in loc_lower for m in ["india", "bangalore", "bengaluru", "mumbai", "delhi", "gurgaon"]):
        countries.append("India")
    if any(m in loc_lower for m in ["poland", "warsaw", "krakow", "wroclaw"]):
        countries.append("Poland")
    if any(m in loc_lower for m in ["singapore"]):
        countries.append("Singapore")
    if any(m in loc_lower for m in ["australia", "sydney", "melbourne"]):
        countries.append("Australia")

    return {
        "is_remote": is_remote,
        "primary_region": primary_region,
        "regions": regions,
        "countries": list(set(countries))
    }


def analyze_interview_process(proc_str: str) -> Dict[str, Any]:
    """Deconstructs the interview process into archetypes, score, and cheat-codes."""
    proc_lower = proc_str.lower()
    
    has_take_home = bool(re.search(r'\b(take[-\s]?home|assignment|exercise|test|coding task|mini[- ]?project|challenge|homework)\b', proc_lower))
    has_pairing = bool(re.search(r'\b(pair[-\s]?programming|pair|pairing|screenshare|screen share|pair with)\b', proc_lower))
    has_architecture = bool(re.search(r'\b(architecture|system design|design discussion|design|tradeoff|trade-off|high level design|hld|lld|technical discussion)\b', proc_lower))
    has_code_review = bool(re.search(r'\b(code review|walkthrough|walk-through|walk through|portfolio|github|past project|hobby|work sample|sample|project review|code sample|previous project)\b', proc_lower))
    has_paid_trial = bool(re.search(r'\b(paid|trial|sprint|contract|bounty)\b', proc_lower))
    has_culture_fit = bool(re.search(r'\b(culture|values|behavioral|soft skills|team connect|lunch|leadership|informal chat|culture fit)\b', proc_lower))

    # Calculate Candidate Friendliness Score (1 to 100)
    score = 75  # Base score for discarding whiteboards
    if has_paid_trial:
        score += 15
    if has_pairing:
        score += 5
    if has_code_review:
        score += 5
    if "guaranteed feedback" in proc_lower or "feedback" in proc_lower:
        score += 5
    if "timeboxed" in proc_lower or "short" in proc_lower or "2-4 hour" in proc_lower or "1 hour" in proc_lower:
        score += 5
    if "own ide" in proc_lower or "personal laptop" in proc_lower:
        score += 5
        
    # Penalty for grueling multi-step gauntlets
    if proc_lower.count("interview") > 5 or proc_lower.count("round") > 5:
        score -= 10
    
    score = min(100, max(50, score))

    # Tech stack extraction
    techs = []
    tech_patterns = [
        "python", "javascript", "typescript", "react", "vue", "angular", "node", "nodejs",
        "go", "golang", "rust", "java", "kotlin", "swift", "c#", ".net", "ruby", "rails",
        "elixir", "clojure", "scala", "php", "magento", "docker", "kubernetes", "aws",
        "graphql", "sql", "postgres", "mysql", "mongodb"
    ]
    for tp in tech_patterns:
        if re.search(r'\b' + re.escape(tp) + r'\b', proc_lower):
            techs.append(tp.capitalize() if len(tp) > 3 else tp.upper())

    # Tactical cheat sheet generation
    tips = []
    if has_paid_trial:
        tips.append("★ Paid Trial: Treat like your first day on the job. Focus on clean git commits, proactive communication, and respecting team PR conventions.")
    if has_take_home:
        tips.append("★ Take-Home Project: Prioritize production hygiene over algorithmic cleverness. Include a comprehensive README.md, clear trade-offs, unit tests, and Docker/env configuration.")
    if has_pairing:
        tips.append("★ Live Pairing: Verbalize your thinking continuously. Ask requirements questions early, treat the interviewer as a team member, and leverage your normal IDE shortcuts and docs.")
    if has_architecture:
        tips.append("★ System Design: Structure around trade-offs: latency vs. consistency, write-heavy vs. read-heavy, data models, failure boundaries, and cost.")
    if has_code_review:
        tips.append("★ Code Walkthrough: Highlight why decisions were made, challenges you surmounted, and what you would do differently in hindsight.")

    if not tips:
        tips.append("★ Practical Discussion: Prepare to speak deeply about past production outages, system architecture you owned, and how you mentor or collaborate.")

    cheat_sheet = " ".join(tips)

    return {
        "has_take_home": has_take_home,
        "has_pairing": has_pairing,
        "has_architecture": has_architecture,
        "has_code_review": has_code_review,
        "has_paid_trial": has_paid_trial,
        "has_culture_fit": has_culture_fit,
        "friendliness_score": score,
        "tech_keywords": sorted(list(set(techs))),
        "cheat_sheet": cheat_sheet
    }


def parse_all_companies(content: str) -> List[Dict[str, Any]]:
    """Parses all companies from README text."""
    lines = content.splitlines()
    skip_phrases = [
        "hackernews", "finding a better alternative", "how to hire engineering",
        "how i hire programmers", "they whiteboarded me!", "open a pr", "recommendations"
    ]
    
    companies = []
    comp_id = 1

    for line in lines:
        line_s = line.strip()
        if not line_s.startswith("- ["):
            continue
            
        low = line_s.lower()
        if any(sp in low for sp in skip_phrases):
            continue

        parts = [p.strip() for p in line_s.split("|")]
        
        name_match = re.search(r'-\s*\[(.*?)\]\((.*?)\)', parts[0])
        if name_match:
            name = name_match.group(1).strip()
            url = name_match.group(2).strip()
        else:
            name_match2 = re.search(r'-\s*\[(.*?)\]', parts[0])
            name = name_match2.group(1).strip() if name_match2 else parts[0].replace("- [", "").replace("]", "").strip()
            url = ""

        if len(parts) == 1:
            raw_loc = ""
            raw_proc = ""
        elif len(parts) == 2:
            raw_loc = parts[1]
            raw_proc = ""
        else:
            raw_loc = parts[1]
            raw_proc = " | ".join(parts[2:])

        geo_meta = parse_locations_and_regions(raw_loc, raw_proc)
        proc_meta = analyze_interview_process(raw_proc)

        # Merge into consolidated record
        record = {
            "id": comp_id,
            "name": name,
            "careers_url": url,
            "raw_location": raw_loc,
            "raw_process": raw_proc,
            "is_remote": geo_meta["is_remote"],
            "primary_region": geo_meta["primary_region"],
            "regions": geo_meta["regions"],
            "countries": geo_meta["countries"],
            "has_take_home": proc_meta["has_take_home"],
            "has_pairing": proc_meta["has_pairing"],
            "has_architecture": proc_meta["has_architecture"],
            "has_code_review": proc_meta["has_code_review"],
            "has_paid_trial": proc_meta["has_paid_trial"],
            "has_culture_fit": proc_meta["has_culture_fit"],
            "friendliness_score": proc_meta["friendliness_score"],
            "tech_keywords": proc_meta["tech_keywords"],
            "cheat_sheet": proc_meta["cheat_sheet"]
        }
        companies.append(record)
        comp_id += 1

    return companies


def export_to_sqlite(companies: List[Dict[str, Any]]):
    """Exports dataset to SQLite with full-text search (FTS5)."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS companies")
    cursor.execute("DROP TABLE IF EXISTS companies_fts")

    cursor.execute("""
        CREATE TABLE companies (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            careers_url TEXT,
            raw_location TEXT,
            raw_process TEXT,
            is_remote INTEGER,
            primary_region TEXT,
            regions_json TEXT,
            countries_json TEXT,
            has_take_home INTEGER,
            has_pairing INTEGER,
            has_architecture INTEGER,
            has_code_review INTEGER,
            has_paid_trial INTEGER,
            has_culture_fit INTEGER,
            friendliness_score INTEGER,
            tech_keywords_json TEXT,
            cheat_sheet TEXT
        )
    """)

    cursor.execute("""
        CREATE VIRTUAL TABLE companies_fts USING fts5(
            id UNINDEXED,
            name,
            raw_location,
            raw_process,
            primary_region,
            cheat_sheet
        )
    """)

    for c in companies:
        cursor.execute("""
            INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["id"],
            c["name"],
            c["careers_url"],
            c["raw_location"],
            c["raw_process"],
            1 if c["is_remote"] else 0,
            c["primary_region"],
            json.dumps(c["regions"]),
            json.dumps(c["countries"]),
            1 if c["has_take_home"] else 0,
            1 if c["has_pairing"] else 0,
            1 if c["has_architecture"] else 0,
            1 if c["has_code_review"] else 0,
            1 if c["has_paid_trial"] else 0,
            1 if c["has_culture_fit"] else 0,
            c["friendliness_score"],
            json.dumps(c["tech_keywords"]),
            c["cheat_sheet"]
        ))

        cursor.execute("""
            INSERT INTO companies_fts VALUES (?, ?, ?, ?, ?, ?)
        """, (
            c["id"],
            c["name"],
            c["raw_location"],
            c["raw_process"],
            c["primary_region"],
            c["cheat_sheet"]
        ))

    conn.commit()
    conn.close()
    print(f"[✓] SQLite database generated: {SQLITE_DB_PATH} ({len(companies)} records)")


def export_to_json_and_csv(companies: List[Dict[str, Any]]):
    """Exports structured data to JSON and CSV."""
    with open(JSON_EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    print(f"[✓] JSON catalog exported: {JSON_EXPORT_PATH}")

    fieldnames = [
        "id", "name", "careers_url", "is_remote", "primary_region", "countries",
        "raw_location", "has_take_home", "has_pairing", "has_architecture",
        "has_code_review", "has_paid_trial", "has_culture_fit", "friendliness_score",
        "tech_keywords", "raw_process", "cheat_sheet"
    ]
    with open(CSV_EXPORT_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in companies:
            row = dict(c)
            row["countries"] = ", ".join(c["countries"])
            row["tech_keywords"] = ", ".join(c["tech_keywords"])
            if "regions" in row:
                del row["regions"]
            writer.writerow(row)
    print(f"[✓] CSV dataset exported: {CSV_EXPORT_PATH}")


def search_companies(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """Runs a full-text search on companies."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    safe_query = re.sub(r'[^a-zA-Z0-9\s]', ' ', query).strip()
    if not safe_query:
        cursor.execute("SELECT * FROM companies LIMIT ?", (limit,))
    else:
        cursor.execute("""
            SELECT c.* FROM companies c
            JOIN companies_fts f ON c.id = f.id
            WHERE companies_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (safe_query, limit))

    rows = cursor.fetchall()
    results = [dict(r) for r in rows]
    conn.close()
    return results


class CockpitHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP server delivering the interactive cockpit and REST API."""
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/api/companies":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if JSON_EXPORT_PATH.exists():
                self.wfile.write(JSON_EXPORT_PATH.read_bytes())
            else:
                self.wfile.write(b"[]")
            return

        if path == "/api/search":
            qs = urllib.parse.parse_qs(parsed.query)
            q = qs.get("q", [""])[0]
            limit = int(qs.get("limit", [50])[0])
            results = search_companies(q, limit=limit)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(results, indent=2).encode("utf-8"))
            return

        # Serve the HTML Cockpit by default for /
        if path in ["/", "/cockpit", "/index.html"]:
            cockpit_file = BASE_DIR / "hiring_without_whiteboards_cockpit.html"
            if cockpit_file.exists():
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(cockpit_file.read_bytes())
                return

        return super().do_GET()


def main():
    parser = argparse.ArgumentParser(description="Hiring Without Whiteboards Deep Engine")
    parser.add_argument("--build", action="store_true", help="Parse README and rebuild SQLite, JSON, CSV datasets")
    parser.add_argument("--stats", action="store_true", help="Display summary statistics")
    parser.add_argument("--search", type=str, help="Search companies by query")
    parser.add_argument("--remote", action="store_true", help="Filter for remote-first / remote-friendly")
    parser.add_argument("--paid-trial", action="store_true", help="Filter for paid trial sprint companies")
    parser.add_argument("--serve", type=int, nargs="?", const=8780, help="Serve the Mission Control Cockpit on port (default 8780)")
    args = parser.parse_args()

    # Rebuild if requested or if data files don't exist
    if args.build or not JSON_EXPORT_PATH.exists() or not SQLITE_DB_PATH.exists():
        print("[*] Parsing raw README data from poteto/hiring-without-whiteboards...")
        readme_content = load_raw_readme()
        companies = parse_all_companies(readme_content)
        print(f"[*] Parsed {len(companies)} validated company entries.")
        export_to_sqlite(companies)
        export_to_json_and_csv(companies)

    if args.stats:
        with open(JSON_EXPORT_PATH, "r", encoding="utf-8") as f:
            comps = json.load(f)
        total = len(comps)
        remote = sum(1 for c in comps if c["is_remote"])
        take_home = sum(1 for c in comps if c["has_take_home"])
        pairing = sum(1 for c in comps if c["has_pairing"])
        arch = sum(1 for c in comps if c["has_architecture"])
        trials = sum(1 for c in comps if c["has_paid_trial"])
        print("\n=======================================================")
        print("  HIRING WITHOUT WHITEBOARDS — EMPIRICAL METRICS")
        print("=======================================================")
        print(f"  Total Companies Cataloged : {total}")
        print(f"  Remote-Friendly Employers : {remote} ({remote/total*100:.1f}%)")
        print(f"  Take-Home Projects / Tasks: {take_home} ({take_home/total*100:.1f}%)")
        print(f"  Live Pair-Programming     : {pairing} ({pairing/total*100:.1f}%)")
        print(f"  Architecture & Past-Work  : {arch} ({arch/total*100:.1f}%)")
        print(f"  Paid Trials / Mini-Sprints: {trials} ({trials/total*100:.1f}%)")
        print("=======================================================\n")

    if args.search:
        results = search_companies(args.search)
        print(f"\nSearch results for '{args.search}' ({len(results)} matches):")
        for r in results:
            rem = "[REMOTE]" if r["is_remote"] else ""
            print(f"  • {r['name']} {rem} ({r['raw_location']}) - Score: {r['friendliness_score']}/100")
            print(f"    URL: {r['careers_url']}")
            print(f"    Process: {r['raw_process'][:120]}...\n")

    if args.serve:
        port = args.serve
        print(f"[*] Launching Hiring Without Whiteboards Cockpit on http://localhost:{port}")
        os.chdir(str(BASE_DIR))
        with socketserver.TCPServer(("", port), CockpitHandler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n[!] Cockpit server stopped.")


if __name__ == "__main__":
    main()
