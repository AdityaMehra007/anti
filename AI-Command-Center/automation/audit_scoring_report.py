"""
Antigravity Career Operations Engine: Full Inventory & Scoring Audit
"""
import json
import os
import sqlite3

VAULT_PATH = os.path.join(os.path.dirname(__file__), "..", "projects", "flagship-career-engine", "career_vault.db")

conn = sqlite3.connect(VAULT_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 1. Total jobs
cur.execute("SELECT COUNT(*) FROM jobs")
total_jobs = cur.fetchone()[0]

# 2. Company breakdown
cur.execute("SELECT company, COUNT(*) as c FROM jobs GROUP BY company ORDER BY c DESC")
companies = cur.fetchall()

# 3. Score distribution
cur.execute("SELECT AVG(fit_score), MIN(fit_score), MAX(fit_score) FROM jobs")
avg_s, min_s, max_s = cur.fetchone()

cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 80")
tier1_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 70 AND fit_score < 80")
tier2_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score >= 60 AND fit_score < 70")
tier3_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM jobs WHERE fit_score < 60")
tier4_count = cur.fetchone()[0]

# 4. Top Tier 1 jobs
cur.execute("""
    SELECT job_id, company, title, location, fit_score, score_breakdown, disqualification_flags
    FROM jobs WHERE fit_score >= 80 ORDER BY fit_score DESC, company ASC
""")
tier1_jobs = cur.fetchall()

# 5. Flagged jobs
cur.execute("""
    SELECT job_id, company, title, fit_score, disqualification_flags
    FROM jobs WHERE disqualification_flags != '[]'
""")
flagged_jobs = cur.fetchall()

# 6. Asset index
asset_index_path = os.path.join(os.path.dirname(__file__), "..", "projects", "flagship-career-engine", "asset_index.json")
mapped_assets = 0
if os.path.exists(asset_index_path):
    with open(asset_index_path, encoding="utf-8") as f:
        assets_data = json.load(f)
        mapped_assets = sum(1 for v in assets_data.values() if any(v.values()))

# Print summary report
print("=" * 70)
print("ANTIGRAVITY CAREER VAULT: COMPREHENSIVE INVENTORY & SCORING AUDIT")
print("=" * 70)
print(f"Total Live Indexed Opportunities: {total_jobs}")
print(f"Total Unique Sponsoring Companies: {len(companies)}")
print(f"Deterministic Average Score:      {avg_s:.2f} / 100 (Min: {min_s}, Max: {max_s})")
print(f"Pre-Configured Mapped Assets:     {mapped_assets} of {total_jobs} roles")
print("-" * 70)
print("SCORE TIER STRATIFICATION:")
print(f"  * Tier 1 (Immediate Priority, >= 80 pts): {tier1_count} roles ({(tier1_count/total_jobs)*100:.1f}%)")
print(f"  * Tier 2 (High Potential, 70-79 pts):     {tier2_count} roles ({(tier2_count/total_jobs)*100:.1f}%)")
print(f"  * Tier 3 (Conditional Fit, 60-69 pts):   {tier3_count} roles ({(tier3_count/total_jobs)*100:.1f}%)")
print(f"  * Tier 4 (Disqualified / Low, < 60 pts): {tier4_count} roles ({(tier4_count/total_jobs)*100:.1f}%)")
print("-" * 70)
print("TOP EMPLOYER REQUISITION VOLUME (TOP 12):")
for c in companies[:12]:
    print(f"  - {c['company']:<35} : {c['c']:>3} requisitions")

print("-" * 70)
print(f"ALL TIER 1 PRIORITY ROLES (FIT SCORE >= 80, TOTAL: {len(tier1_jobs)}):")
for idx, r in enumerate(tier1_jobs, 1):
    sb = json.loads(r["score_breakdown"]) if r["score_breakdown"] else {}
    print(f"  {idx:>2}. [{r['fit_score']:>2} pts] {r['company']} - {r['title']}")
    print(f"      Location: {r['location']} | Job ID: {r['job_id']}")

print("-" * 70)
print(f"DISQUALIFICATION & WARNING FLAGS ({len(flagged_jobs)} ROLES):")
for f in flagged_jobs:
    flags = json.loads(f["disqualification_flags"])
    print(f"  - [{f['fit_score']} pts] {f['company']} | {f['title']} -> {flags}")

print("=" * 70)
conn.close()
