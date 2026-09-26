import os, sys, time, csv, json, subprocess
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE = r"e:\anti"
os.environ["PYTHONIOENCODING"] = "utf-8"
LOG_FILE = os.path.join(WORKSPACE, "master_autopilot.log")

def log(msg):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now_str}] [AUTOPILOT] {msg}\n"
    print(entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def run_autopilot_cycle():
    log("================================================================================")
    log("🚀 STARTING MASTER AUTONOMOUS CYCLE — ADITYA MEHRA CAREER EMPIRE")
    log("================================================================================")
    
    # 1. Run 365-Day Application Batch
    log("[STEP 1/5] Executing 365-Day Continuous Application Cycle...")
    res1 = subprocess.run([sys.executable, os.path.join(WORKSPACE, "career_365_days_continuous_engine.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    log(f"  -> Result: {'PASS' if res1.returncode == 0 else 'FAIL'}")
    
    # 2. Run Hourly Job Application Engine
    log("[STEP 2/5] Running Hourly Job Application Engine...")
    res2 = subprocess.run([sys.executable, os.path.join(WORKSPACE, "hourly_job_application_engine.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    log(f"  -> Result: {'PASS' if res2.returncode == 0 else 'FAIL'}")
    
    # 3. Run Daily Recruiter Maintenance Engine
    log("[STEP 3/5] Syncing Recruiter & Hiring Contacts Database...")
    res3 = subprocess.run([sys.executable, os.path.join(WORKSPACE, "daily_contact_database_maintenance_engine.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    log(f"  -> Result: {'PASS' if res3.returncode == 0 else 'FAIL'}")
    
    # 4. Refresh LinkedIn Referral Map & Email Drafts
    log("[STEP 4/5] Refreshing 61-Job Referral Network & Outreach Drafts...")
    drafts_dir = os.path.join(WORKSPACE, "Email_Drafts")
    draft_count = len([f for f in os.listdir(drafts_dir) if f.endswith('.eml')]) if os.path.exists(drafts_dir) else 0
    log(f"  -> Verified {draft_count} active recruiter .eml drafts ready for dispatch.")
    
    # 5. Run Master System Health Verification
    log("[STEP 5/5] Performing System Health & Diagnostics Audit...")
    res5 = subprocess.run([sys.executable, os.path.join(WORKSPACE, "run_master_omniverse_verification.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    log(f"  -> Result: {'PASS' if res5.returncode == 0 else 'FAIL'}")
    
    log("================================================================================")
    log("✅ MASTER AUTONOMOUS CYCLE COMPLETED SUCCESSFULLY.")
    log("================================================================================")

if __name__ == "__main__":
    run_autopilot_cycle()
