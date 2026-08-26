"""
OMEGA ULTRA - Optimized Forensic Workspace Inspector
Scans all production files, databases, lines of code, git commits, and directories to provide exact ground truth data.
"""
import os
import sys
import sqlite3
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(r"e:\anti")
SKIP_DIRS = {".git", "wshobson-agents", ".agents", "claude-plugins-community", "external", "ai-engineering-from-scratch"}

def run_forensic_scan():
    # 1. Databases analysis
    dbs = []
    for p in WORKSPACE.rglob("*.db"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        dbs.append(p)

    db_report = []
    for db in dbs:
        try:
            conn = sqlite3.connect(str(db))
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [r[0] for r in cur.fetchall()]
            table_counts = {}
            for t in tables:
                try:
                    cur.execute(f'SELECT COUNT(*) FROM "{t}"')
                    table_counts[t] = cur.fetchone()[0]
                except Exception as e:
                    table_counts[t] = str(e)
            conn.close()
            db_report.append({
                "path": str(db.relative_to(WORKSPACE)),
                "size_bytes": db.stat().st_size,
                "tables": table_counts
            })
        except Exception as e:
            db_report.append({"path": str(db.relative_to(WORKSPACE)), "error": str(e)})

    # 2. File stats by extension and directory
    ext_stats = {}
    dir_stats = {}
    total_files = 0
    total_lines = 0

    for p in WORKSPACE.rglob("*"):
        if any(skip in p.parts for skip in SKIP_DIRS):
            continue
        if p.is_file():
            total_files += 1
            ext = p.suffix.lower() or "no_ext"
            ext_stats[ext] = ext_stats.get(ext, 0) + 1
            top_dir = p.relative_to(WORKSPACE).parts[0] if len(p.relative_to(WORKSPACE).parts) > 1 else "root"
            dir_stats[top_dir] = dir_stats.get(top_dir, 0) + 1
            if ext in [".py", ".js", ".html", ".css", ".md", ".json", ".csv", ".txt"]:
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass

    # 3. Git commit history
    try:
        git_log = subprocess.run(["git", "log", "--oneline"], cwd=WORKSPACE, capture_output=True, text=True).stdout.strip().split("\n")
    except Exception as e:
        git_log = [str(e)]

    # 4. HTML Dashboard Discovery
    html_files = [str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("*.html") if not any(skip in p.parts for skip in SKIP_DIRS)]

    # 5. Test Suites Discovery
    test_files = [str(p.relative_to(WORKSPACE)) for p in WORKSPACE.rglob("test_*.py") if not any(skip in p.parts for skip in SKIP_DIRS)]

    out = {
        "total_files": total_files,
        "total_lines_of_code_and_docs": total_lines,
        "extension_counts": ext_stats,
        "directory_counts": dir_stats,
        "database_count": len(db_report),
        "databases": db_report,
        "git_commits_count": len(git_log) if git_log and git_log[0] else 0,
        "git_commits": git_log,
        "html_dashboards_count": len(html_files),
        "html_dashboards": html_files,
        "test_files_count": len(test_files),
        "test_files": test_files
    }

    with open(WORKSPACE / "apex" / "FORENSIC_RAW_DATA.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print(f"[FORENSIC_SCAN_COMPLETE] Total Production Files: {total_files}, Lines: {total_lines}, DBs: {len(db_report)}, Dashboards: {len(html_files)}, Tests: {len(test_files)}")

if __name__ == "__main__":
    run_forensic_scan()
