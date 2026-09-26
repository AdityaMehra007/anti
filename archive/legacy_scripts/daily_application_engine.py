# -*- coding: utf-8 -*-
import json
import sqlite3
import datetime
from pathlib import Path

def run_daily_sprint():
    today_str = datetime.date.today().isoformat()
    batch_dir = Path(f'E:/anti/daily_batches/{today_str}')
    batch_dir.mkdir(parents=True, exist_ok=True)

    v_profile = json.loads(Path('E:/anti/verified_profile.json').read_text(encoding='utf-8'))
    cand = v_profile['candidate']

    conn = sqlite3.connect('E:/anti/omega_career_database.sqlite')
    cur = conn.cursor()

    print("=" * 80)
    print(f"??? OMEGA DAILY APPLICATION DISPATCH: {today_str}")
    print(f"Candidate: {cand['full_name']} | Target: Bengaluru Operations & Strategy")
    print("=" * 80)

    rows = cur.execute('SELECT DISTINCT company, title, fit_score, eov_score, interview_prob, tier, dossier_path FROM job_pipeline ORDER BY eov_score DESC').fetchall()
    
    print(f"\n?? TODAY'S ACTIVE STAGED SUBMISSION QUEUE ({len(rows)} Target Roles):\n")
    for i, r in enumerate(rows, 1):
        print(f"  {i}. [{r[5]:<2}] {r[0]:<18} | {r[1]:<38} | Fit: {r[2]:.1f}% | Prob: {r[4]}")
        print(f"     ?? Dossier: {r[6]}")
        print()

    cur.execute("""
    INSERT INTO audit_ledger (event_type, entity_id, details)
    VALUES ('DAILY_RUN_CHECK', 'SYSTEM', ?)
    """, (f"Daily dispatch executed for {today_str} across {len(rows)} active opportunities.",))
    
    conn.commit()
    conn.close()

    print("=" * 80)
    print("?? EXECUTION STEPS:")
    print(f"  1. Open each dossier in E:/anti/daily_batches/{today_str}/")
    print("  2. Attach Master CV: E:/ai-job-search/cv/Aditya_Mehra_Master_CV.tex")
    print("  3. Send direct LinkedIn outreach note to the company recruiter")
    print("=" * 80)

if __name__ == '__main__':
    run_daily_sprint()
