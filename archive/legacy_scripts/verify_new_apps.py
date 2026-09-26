import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

app_files = [
    "e:/anti/apps/bangalore_commute/index.html",
    "e:/anti/apps/ats_scanner/index.html",
    "e:/anti/apps/email_composer/index.html",
    "e:/anti/apps/portfolio_pdf/index.html",
    "e:/anti/apps/index.html"
]

print("=== VERIFYING ADI SOVEREIGN OS APPS SUITE ===")
all_ok = True
for fpath in app_files:
    if os.path.exists(fpath):
        size = os.path.getsize(fpath)
        print(f"[OK] {fpath} ({size:,} bytes)")
    else:
        print(f"[FAIL] {fpath} not found!")
        all_ok = False

if all_ok:
    print("\nALL 5 REQUIRED DELIVERABLES VERIFIED SUCCESSFULLY!")
else:
    print("\nSOME DELIVERABLES ARE MISSING!")
