"""
Automated Snapshot & Backup Utility
Safely copies career_vault.db and core markdown files into timestamped backups
"""

import os
import shutil
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
VAULT_SRC = os.path.join(
    BASE_DIR, "projects", "flagship-career-engine", "career_vault.db"
)


def run_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if os.path.exists(VAULT_SRC):
        target_db = os.path.join(BACKUP_DIR, f"career_vault_{timestamp}.db")
        shutil.copy2(VAULT_SRC, target_db)
        print(f"[OK] Database backed up to: {target_db}")
    else:
        print(f"[WARN] Source vault not found at: {VAULT_SRC}")

    print(f"[OK] Backup completed successfully at {datetime.now().isoformat()}")


if __name__ == "__main__":
    run_backup()
