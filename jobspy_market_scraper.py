"""
JobSpy Bangalore Market Intelligence & Autonomous Sourcing Engine
Wraps speedyapply/JobSpy to scrape, normalize, score, deduplicate, and ingest
live job opportunities across LinkedIn, Indeed, Glassdoor, Google Jobs, and Naukri.

Candidate Ground Truth: Aditya Mehra (DSU Bangalore '26)
Evidence Base: EXP-001 (AI Data), EXP-002 (B2B BD / INR 1.5L+), EXP-003 (AERO India Lead Gen)
"""

import os
import re
import sys
import csv
import json
import logging
import argparse
import concurrent.futures
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Setup Logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")
logger = logging.getLogger("JobSpyEngine")

# Workspace Paths
WORKSPACE = Path(r"e:\anti")
DATA_DIR = WORKSPACE / "data"
SCRAPES_DIR = DATA_DIR / "jobspy_scrapes"
JOB_APPLICATIONS_CSV = WORKSPACE / "job_applications.csv"
ACTIVE_STRIKE_BOARD_MD = WORKSPACE / "ACTIVE_HIRING_MNC_STRIKE_BOARD.md"
CANDIDATE_DIR = WORKSPACE / "career-hub" / "candidate"
MARKET_MAP_JSON = CANDIDATE_DIR / "bangalore_market_map.json"

BANGALORE_CLUSTERS = [
    {
        "name": "Outer Ring Road (Bellandur / Marathahalli / Sarjapur)",
        "keywords": ["bellandur", "outer ring road", "orr", "marathahalli", "sarjapur", "kadubeesanahalli", "devarabisanahalli", "ecospace", "embassy techvillage"]
    },
    {
        "name": "Whitefield & ITPL",
        "keywords": ["whitefield", "itpl", "hoodi", "kadugodi", "export promotion industrial park", "epip"]
    },
    {
        "name": "Manyata Tech Park (Hebbal)",
        "keywords": ["manyata", "hebbal", "nagavara", "thanisandra"]
    },
    {
        "name": "Koramangala & HSR Layout",
        "keywords": ["koramangala", "hsr", "hsr layout", "btm", "ejipura", "sony world"]
    },
    {
        "name": "Electronic City (Phase 1 & 2)",
        "keywords": ["electronic city", "electronic city phase", "ecity", "bommasandra"]
    },
    {
        "name": "CBD (MG Road / Indiranagar / Richmond)",
        "keywords": ["mg road", "m.g. road", "indiranagar", "richmond", "residency road", "lavelle road", "church street", "cbd", "cubbon"]
    }
]

TARGET_ROLES_DEFAULT = [
    "Business Development Executive",
    "B2B Sales Specialist",
    "AI Operations Associate",
    "AI Data Specialist",
    "International Business Executive",
    "Founders Office Associate"
]


def detect_bangalore_cluster(location_str: Optional[str]) -> str:
    """Classifies a Bangalore location string into one of 6 tech corridors or general corridor."""
    if not location_str:
        return "Bengaluru General Corridor"

    loc_lower = location_str.lower()
    for cluster in BANGALORE_CLUSTERS:
        for kw in cluster["keywords"]:
            if kw in loc_lower:
                return cluster["name"]

    if any(city in loc_lower for city in ["bengaluru", "bangalore", "ka, in", "karnataka"]):
        return "Bengaluru General Corridor"

    return location_str.strip()


def normalize_job_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw JobSpy output into standardized dictionary."""
    comp_raw = raw.get("company") or raw.get("company_name")
    if not comp_raw or str(comp_raw).strip().lower() in ["nan", "none", "null", ""]:
        company = "Confidential Employer"
    else:
        company = str(comp_raw).strip()

    title = str(raw.get("title") or "Unknown Title").strip()
    loc_raw = str(raw.get("location") or "Bengaluru, Karnataka, India").strip()
    if loc_raw.lower() in ["nan", "none", "ka, in", "karnataka, india"]:
        loc_raw = "Bengaluru, Karnataka, India"

    cluster = detect_bangalore_cluster(loc_raw)

    site_raw = str(raw.get("site") or "").lower()
    site_map = {
        "linkedin": "LinkedIn",
        "indeed": "Indeed",
        "naukri": "Naukri",
        "glassdoor": "Glassdoor",
        "google": "Google Jobs",
        "zip_recruiter": "ZipRecruiter",
        "bayt": "Bayt",
        "bdjobs": "Bdjobs"
    }
    site = site_map.get(site_raw, site_raw.capitalize() if site_raw else "Direct Portal")

    # Pick direct application URL if available
    job_url_direct = str(raw.get("job_url_direct") or "").strip()
    job_url = str(raw.get("job_url") or "").strip()
    app_url = job_url_direct if job_url_direct and job_url_direct.startswith("http") else job_url

    desc = str(raw.get("description") or "").strip()

    loc_display = f"Bengaluru ({cluster.split('(')[0].strip()})" if "Bengaluru" not in cluster else cluster

    return {
        "id": str(raw.get("id") or ""),
        "company": company,
        "title": title,
        "location": loc_display,
        "raw_location": loc_raw,
        "cluster": cluster,
        "site": site,
        "application_url": app_url,
        "salary_min": raw.get("min_amount"),
        "salary_max": raw.get("max_amount"),
        "interval": raw.get("interval"),
        "currency": raw.get("currency") or "INR",
        "description": desc,
        "date_posted": str(raw.get("date_posted") or datetime.now().strftime("%Y-%m-%d")),
        "is_remote": bool(raw.get("is_remote", False))
    }


def calculate_role_fit_score(job: Dict[str, Any]) -> Tuple[int, List[str], str]:
    """
    Calculates candidate alignment score (0-100) based on Aditya Mehra's verified evidence:
      EXP-001: Instawork AI Data (LLM, annotation, evaluation, data operations)
      EXP-002: Pencil Mark BD (B2B sales, outbound, INR 1.5L+ closed pipeline)
      EXP-003: AERO India 2025 (Lead generation, international B2B outreach)
    """
    title_lower = job["title"].lower()
    desc_lower = job["description"].lower()
    text = f"{title_lower} {desc_lower}"

    score = 50
    evidence = []
    reasons = []

    # Track 1: B2B Sales / Business Development / Account Exec / SDR
    b2b_kws = ["business development", "b2b", "sales", "outbound", "lead generation", "pipeline", "client acquisition", "sdr", "bdr", "partnerships", "cold outreach"]
    b2b_matches = [kw for kw in b2b_kws if kw in text]
    if b2b_matches:
        score += 25
        evidence.append("EXP-002")
        evidence.append("EXP-003")
        reasons.append("B2B sales & outbound pipeline alignment (Pencil Mark / AERO India)")

    # Track 2: AI Operations / AI Data / Prompt Engineering / LLM Ops
    ai_kws = ["ai", "annotation", "data labeling", "prompt", "llm", "curation", "eval", "evaluation", "benchmark", "quality audit", "machine learning operations", "ai data"]
    ai_matches = [kw for kw in ai_kws if kw in text]
    if ai_matches:
        score += 25
        if "EXP-001" not in evidence:
            evidence.append("EXP-001")
        reasons.append("AI data annotation & evaluation alignment (Instawork AI Data)")

    # Track 3: International Trade / EXIM / Cross-Border / Supply Chain
    trade_kws = ["international business", "exim", "export", "import", "customs", "cross-border", "incoterms", "freight", "logistics", "trade operations"]
    trade_matches = [kw for kw in trade_kws if kw in text]
    if trade_matches:
        score += 20
        reasons.append("BBA International Business degree & trade operations capability")

    # Track 4: Founders Office / Growth / Strategic Operations
    growth_kws = ["founder's office", "founders office", "growth associate", "business operations", "bizops", "strategy associate"]
    growth_matches = [kw for kw in growth_kws if kw in text]
    if growth_matches:
        score += 15
        reasons.append("Strategic growth & cross-functional operations fit")

    # Seniority evaluation
    if any(kw in title_lower for kw in ["senior", "principal", "staff", "architect", "director", "vp", "head"]):
        score -= 40
        reasons.append("Seniority mismatch (high-experience role)")
    elif "15+ years" in text or "10+ years" in text or "8+ years" in text:
        score -= 35
        reasons.append("Requires extensive executive/staff years")
    else:
        fresher_kws = ["fresher", "entry level", "junior", "associate", "graduate", "0-1 year", "0-2 years", "0-3 years", "intern"]
        if any(kw in text for kw in fresher_kws):
            score += 10
            reasons.append("Fresher / entry-level friendly")

    # Geo-Cluster Boost
    if job.get("cluster") and job["cluster"] != "Bengaluru General Corridor":
        score += 5
        reasons.append(f"Bangalore Hot Corridor ({job['cluster']})")

    score = max(25, min(score, 98))
    rationale = f"Target role fit: {score}/100. Focus: {', '.join(reasons[:2])}."
    return score, evidence, rationale


def deduplicate_jobs(new_jobs: List[Dict[str, Any]], existing_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filters out jobs that already exist by company + title similarity or application URL."""
    existing_keys = set()
    existing_urls = set()

    def clean_str(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", str(s).lower())

    for ej in existing_jobs:
        comp = clean_str(ej.get("Company Name") or ej.get("company") or "")
        title = clean_str(ej.get("Role Title") or ej.get("title") or "")
        url = str(ej.get("Application URL") or ej.get("application_url") or "").strip().rstrip("/")

        if comp and title:
            existing_keys.add((comp, title))
        if url:
            existing_urls.add(url.lower())

    unique = []
    for job in new_jobs:
        comp = clean_str(job.get("company", ""))
        title = clean_str(job.get("title", ""))
        url = str(job.get("application_url", "")).strip().rstrip("/").lower()

        if url and url in existing_urls:
            continue
        if comp and title and (comp, title) in existing_keys:
            continue

        unique.append(job)
        if comp and title:
            existing_keys.add((comp, title))
        if url:
            existing_urls.add(url)

    return unique


def format_for_job_applications_csv(job: Dict[str, Any], fit_score: int, fit_rationale: str) -> Dict[str, str]:
    """Converts a normalized job into a row dictionary conforming to job_applications.csv."""
    today = datetime.now().strftime("%Y-%m-%d")
    follow_up = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

    loc = job["location"]
    if job.get("is_remote"):
        loc += " (Remote)"

    return {
        "Date": today,
        "Company Name": job["company"],
        "Role Title": job["title"],
        "Location/Remote": loc,
        "Job Board / Portal": job["site"],
        "Application URL": job["application_url"],
        "Status": "READY_TO_APPLY",
        "Follow-Up Date": follow_up,
        "Contact Person": "Talent Acquisition Partner",
        "Notes": fit_rationale
    }


def load_existing_job_applications(csv_path: Path) -> List[Dict[str, str]]:
    """Loads existing records from job_applications.csv safely."""
    if not csv_path.exists():
        return []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        logger.warning(f"Could not read existing applications from {csv_path}: {e}")
        return []


def append_to_job_applications_csv(csv_path: Path, new_rows: List[Dict[str, str]]) -> int:
    """Appends new applications to job_applications.csv atomically without overwriting."""
    if not new_rows:
        return 0

    fieldnames = [
        "Date", "Company Name", "Role Title", "Location/Remote",
        "Job Board / Portal", "Application URL", "Status",
        "Follow-Up Date", "Contact Person", "Notes"
    ]

    file_exists = csv_path.exists()
    mode = "a" if file_exists else "w"

    with open(csv_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writeheader()
        for row in new_rows:
            writer.writerow(row)

    logger.info(f"Successfully appended {len(new_rows)} new opportunities to {csv_path}")
    return len(new_rows)


def sync_to_active_strike_board(strike_board_path: Path, jobs: List[Dict[str, Any]]) -> int:
    """Appends high-scoring jobs as live strike targets in ACTIVE_HIRING_MNC_STRIKE_BOARD.md."""
    if not strike_board_path.exists() or not jobs:
        return 0

    try:
        with open(strike_board_path, "r", encoding="utf-8") as f:
            content = f.read()

        appended_count = 0
        new_lines = []
        for i, job in enumerate(jobs):
            comp = job["company"]
            title = job["title"]
            url = job["application_url"]
            if comp in content and title in content:
                continue

            job_id = f"BLR-LIVE-{datetime.now().strftime('%m%d')}-{i+1:02d}"
            table_row = f"| `{job_id}` | **{comp}** | {title} | **Live** | [Apply via {job['site']}]({url}) | Talent Acquisition Team |"
            new_lines.append(table_row)
            appended_count += 1

        if new_lines:
            updated_content = content.rstrip() + "\n" + "\n".join(new_lines) + "\n"
            with open(strike_board_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            logger.info(f"Synced {appended_count} live postings to {strike_board_path.name}")
        return appended_count
    except Exception as e:
        logger.error(f"Error syncing to strike board: {e}")
        return 0


class JobSpyIngestionEngine:
    """Autonomous live scraper and scoring orchestrator wrapping speedyapply/JobSpy."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or SCRAPES_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def scrape(
        self,
        roles: Optional[List[str]] = None,
        sites: Optional[List[str]] = None,
        location: str = "Bengaluru, Karnataka, India",
        results_per_role: int = 15,
        hours_old: int = 72,
        country_indeed: str = "India",
        proxies: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Executes JobSpy scraping across configured boards and roles."""
        roles = roles or TARGET_ROLES_DEFAULT
        sites = sites or ["linkedin", "indeed", "naukri", "glassdoor", "google"]
        all_raw_jobs = []

        try:
            from jobspy import scrape_jobs
        except ImportError as e:
            logger.error(f"JobSpy not installed or missing dependencies: {e}")
            return []

        for role in roles:
            logger.info(f"Querying boards {sites} for role '{role}' in '{location}'...")
            try:
                df = scrape_jobs(
                    site_name=sites,
                    search_term=role,
                    google_search_term=f"{role} jobs in Bengaluru since yesterday" if "google" in sites else None,
                    location=location,
                    results_wanted=results_per_role,
                    hours_old=hours_old,
                    country_indeed=country_indeed,
                    proxies=proxies,
                    verbose=0
                )
                if df is not None and not df.empty:
                    records = df.to_dict(orient="records")
                    logger.info(f"Retrieved {len(records)} postings for role '{role}'")
                    all_raw_jobs.extend(records)
                else:
                    logger.info(f"Zero postings returned for role '{role}'")
            except Exception as ex:
                logger.warning(f"Notice during scrape for role '{role}': {ex}")

        return all_raw_jobs

    def process_and_enrich(
        self,
        raw_records: List[Dict[str, Any]],
        min_fit_score: int = 78
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
        """Normalizes, scores, and filters jobs meeting the fit threshold."""
        existing_apps = load_existing_job_applications(JOB_APPLICATIONS_CSV)
        normalized = [normalize_job_record(r) for r in raw_records]
        deduped = deduplicate_jobs(normalized, existing_apps)

        qualified_jobs = []
        app_rows = []

        for job in deduped:
            score, evidence, rationale = calculate_role_fit_score(job)
            job["fit_score"] = score
            job["matched_evidence"] = evidence
            job["fit_rationale"] = rationale

            if score >= min_fit_score:
                qualified_jobs.append(job)
                app_rows.append(format_for_job_applications_csv(job, score, rationale))

        # Save snapshot to data directory
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_json = self.output_dir / f"jobspy_enriched_{ts}.json"
        with open(snapshot_json, "w", encoding="utf-8") as f:
            json.dump(qualified_jobs, f, indent=2, default=str)

        logger.info(f"Enriched {len(deduped)} deduped jobs. {len(qualified_jobs)} qualified (Score >= {min_fit_score}).")
        return qualified_jobs, app_rows


def main():
    parser = argparse.ArgumentParser(description="JobSpy Bangalore Live Career Ingestion")
    parser.add_argument("--roles", nargs="+", default=None, help="Target roles to search")
    parser.add_argument("--sites", nargs="+", default=None, help="Job boards (linkedin, indeed, naukri, glassdoor, google)")
    parser.add_argument("--limit", type=int, default=10, help="Results wanted per role")
    parser.add_argument("--hours", type=int, default=72, help="Max hours old for postings")
    parser.add_argument("--min-score", type=int, default=80, help="Minimum fit score to qualify")
    parser.add_argument("--dry-run", action="store_true", help="Run search without writing to job_applications.csv")
    parser.add_argument("--sync-board", action="store_true", help="Also sync high-fit jobs to ACTIVE_HIRING_MNC_STRIKE_BOARD.md")
    args = parser.parse_args()

    engine = JobSpyIngestionEngine()
    print("\n=======================================================")
    print("  JOBSPY BANGALORE CAREER INTELLIGENCE & INGESTION")
    print("=======================================================\n")

    raw_jobs = engine.scrape(
        roles=args.roles,
        sites=args.sites,
        results_per_role=args.limit,
        hours_old=args.hours
    )

    qualified, app_rows = engine.process_and_enrich(raw_jobs, min_fit_score=args.min_score)

    print(f"\n[SUMMARY] Total Scraped: {len(raw_jobs)} | Qualified: {len(qualified)}")
    for q in qualified[:8]:
        print(f" -> [{q['site']}] {q['company']} - {q['title']} (Fit: {q['fit_score']}) | {q['cluster']}")

    if not args.dry_run and app_rows:
        count = append_to_job_applications_csv(JOB_APPLICATIONS_CSV, app_rows)
        print(f"\n[STATUS] Injected {count} verified roles into {JOB_APPLICATIONS_CSV.name}!")
        if args.sync_board:
            synced = sync_to_active_strike_board(ACTIVE_STRIKE_BOARD_MD, qualified)
            print(f"[STATUS] Synced {synced} opportunities to {ACTIVE_STRIKE_BOARD_MD.name}!")
    elif args.dry_run:
        print("\n[DRY RUN] Skipped writing to production files.")


if __name__ == "__main__":
    main()
