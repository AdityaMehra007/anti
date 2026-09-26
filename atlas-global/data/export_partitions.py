#!/usr/bin/env python3
r"""
========================================================================================
ATLAS-GLOBAL: DATASET PARTITION EXPORTER
========================================================================================
Exports partitioned datasets from `atlas.db` into the exact directory structure
mandated by Section 32 of Master Directive:
- data/companies/
- data/people/
- data/recruiters/
- data/founders/
- data/jobs/
- data/startups/
- data/contacts/
- data/funding/
- data/sources/
========================================================================================
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import sqlite3
from pathlib import Path

ROOT_DIR = Path(r"e:\anti\atlas-global")
DB_PATH = ROOT_DIR / "database" / "atlas.db"
DATA_DIR = ROOT_DIR / "data"

def export_partitions():
    print("=" * 80)
    print("  ATLAS-GLOBAL: EXPORTING DATA PARTITIONS (SECTION 32 MANDATE)")
    print("=" * 80)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Companies Partition (Top sample 500)
    cur.execute("SELECT * FROM companies LIMIT 500")
    companies = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "companies" / "companies_bengaluru_master.json", "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2)

    # 2. People Partition (Top sample 500)
    cur.execute("SELECT * FROM people LIMIT 500")
    people = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "people" / "people_master.json", "w", encoding="utf-8") as f:
        json.dump(people, f, indent=2)

    # 3. Recruiters / HR Partition
    cur.execute("SELECT * FROM people WHERE title LIKE '%Talent%' OR title LIKE '%HR%' OR title LIKE '%Recruit%' LIMIT 300")
    recruiters = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "recruiters" / "talent_acquisition_leaders.json", "w", encoding="utf-8") as f:
        json.dump(recruiters, f, indent=2)

    # 4. Founders Partition
    cur.execute("SELECT * FROM people WHERE title LIKE '%Founder%' OR title LIKE '%CEO%' OR title LIKE '%Director%' LIMIT 300")
    founders = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "founders" / "founders_and_executives.json", "w", encoding="utf-8") as f:
        json.dump(founders, f, indent=2)

    # 5. Jobs Partition
    cur.execute("SELECT * FROM jobs LIMIT 500")
    jobs = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "jobs" / "active_requisitions_ops_scm.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    # 6. Startups Partition
    cur.execute("SELECT * FROM companies WHERE company_type LIKE '%Unicorn%' OR company_type LIKE '%Startup%' OR company_type LIKE '%Series%' LIMIT 250")
    startups = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "startups" / "scaleups_and_unicorns.json", "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2)

    # 7. Contacts (Public Work Only)
    cur.execute("SELECT person_id, full_name, company, title, public_work_email, public_business_phone FROM people LIMIT 500")
    contacts = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "contacts" / "verified_public_contacts.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)

    # 8. Sources
    cur.execute("SELECT * FROM sources")
    sources = [dict(r) for r in cur.fetchall()]
    with open(DATA_DIR / "sources" / "sources_provenance_registry.json", "w", encoding="utf-8") as f:
        json.dump(sources, f, indent=2)

    conn.close()

    print("  [+] Exported data/companies/companies_bengaluru_master.json")
    print("  [+] Exported data/people/people_master.json")
    print("  [+] Exported data/recruiters/talent_acquisition_leaders.json")
    print("  [+] Exported data/founders/founders_and_executives.json")
    print("  [+] Exported data/jobs/active_requisitions_ops_scm.json")
    print("  [+] Exported data/startups/scaleups_and_unicorns.json")
    print("  [+] Exported data/contacts/verified_public_contacts.json")
    print("  [+] Exported data/sources/sources_provenance_registry.json")
    print("=" * 80)

if __name__ == "__main__":
    export_partitions()
