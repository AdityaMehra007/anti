import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import sqlite3
import subprocess
import datetime
import csv

ROOT = r"e:\anti"
OUTPUT_DIR = os.path.join(ROOT, "omega_ultra_audit")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scan_filesystem():
    print("[1/6] Scanning filesystem...")
    file_inventory = []
    category_counts = {}
    ext_counts = {}
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fpath, ROOT).replace("\\", "/")
            try:
                stat = os.stat(fpath)
                size_bytes = stat.st_size
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat()
                ctime = datetime.datetime.fromtimestamp(stat.st_ctime, tz=datetime.timezone.utc).isoformat()
                ext = os.path.splitext(fname)[1].lower() or "no_ext"
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
                
                classification = "CORE"
                if "scratch" in rel_path.lower() or "temp" in rel_path.lower():
                    classification = "SCRATCH"
                elif "test" in rel_path.lower() or fname.startswith("test_"):
                    classification = "TEST"
                elif rel_path.endswith(".log"):
                    classification = "ACTIVE_LOG"
                elif rel_path.endswith(".json") and "state" in rel_path.lower():
                    classification = "ACTIVE_STATE"
                elif rel_path.startswith("apps/"):
                    classification = "APP_LAYER"
                elif rel_path.startswith("omega/"):
                    classification = "OMEGA_CORE"
                elif rel_path.startswith(".agents/"):
                    classification = "SKILL_SYSTEM"
                elif rel_path.endswith(".csv"):
                    classification = "DATA_CSV"
                elif rel_path.endswith(".md"):
                    classification = "DOCUMENTATION"
                
                category_counts[classification] = category_counts.get(classification, 0) + 1
                
                file_inventory.append({
                    "path": rel_path,
                    "abs_path": fpath,
                    "size_bytes": size_bytes,
                    "created_at": ctime,
                    "modified_at": mtime,
                    "extension": ext,
                    "classification": classification
                })
            except Exception as e:
                pass
                
    return file_inventory, ext_counts, category_counts

def inspect_databases():
    print("[2/6] Inspecting databases...")
    db_results = []
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if fname.endswith(".db") or fname.endswith(".sqlite") or fname.endswith(".sqlite3"):
                db_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(db_path, ROOT).replace("\\", "/")
                db_info = {
                    "path": rel_path,
                    "size_bytes": os.path.getsize(db_path),
                    "tables": {},
                    "error": None
                }
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
                    for t in tables:
                        cnt = cursor.execute(f"SELECT COUNT(*) FROM \"{t}\";").fetchone()[0]
                        cols = [c[1] for c in cursor.execute(f"PRAGMA table_info(\"{t}\");").fetchall()]
                        db_info["tables"][t] = {
                            "row_count": cnt,
                            "columns": cols
                        }
                    conn.close()
                except Exception as e:
                    db_info["error"] = str(e)
                db_results.append(db_info)
    return db_results

def inspect_csvs():
    print("[3/6] Inspecting CSV files...")
    csv_results = []
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for fname in filenames:
            if fname.endswith(".csv"):
                csv_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(csv_path, ROOT).replace("\\", "/")
                csv_info = {
                    "path": rel_path,
                    "size_bytes": os.path.getsize(csv_path),
                    "row_count": 0,
                    "headers": [],
                    "sample": []
                }
                try:
                    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
                        reader = csv.reader(f)
                        headers = next(reader, [])
                        csv_info["headers"] = headers
                        rows = list(reader)
                        csv_info["row_count"] = len(rows)
                        if rows:
                            csv_info["sample"] = rows[0]
                except Exception as e:
                    csv_info["error"] = str(e)
                csv_results.append(csv_info)
    return csv_results

def inspect_git():
    print("[4/6] Inspecting Git history...")
    git_info = {
        "is_repo": False,
        "branches": [],
        "commit_count": 0,
        "recent_commits": [],
        "status_summary": []
    }
    try:
        log_res = subprocess.run(["git", "log", "--pretty=format:%h|%an|%ad|%s", "--date=iso", "-n", "50"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if log_res.returncode == 0 and log_res.stdout.strip():
            git_info["is_repo"] = True
            commits = []
            for line in log_res.stdout.strip().split("\n"):
                parts = line.split("|")
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": "|".join(parts[3:])
                    })
            git_info["recent_commits"] = commits
            git_info["commit_count"] = len(commits)
            
        status_res = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        if status_res.returncode == 0:
            git_info["status_summary"] = status_res.stdout.strip().split("\n")[:30]
    except Exception as e:
        git_info["error"] = str(e)
    return git_info

def inspect_logs():
    print("[5/6] Inspecting logs and daemons...")
    log_files = []
    for fname in ["hourly_job_application.log", "365_days_career_loop.log", "master_autopilot.log", "247_career_loop.log"]:
        fpath = os.path.join(ROOT, fname)
        if os.path.exists(fpath):
            stat = os.stat(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            log_files.append({
                "name": fname,
                "path": fpath,
                "size_bytes": stat.st_size,
                "line_count": len(lines),
                "mtime": datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).isoformat(),
                "head": [l.strip() for l in lines[:5]],
                "tail": [l.strip() for l in lines[-5:]]
            })
    return log_files

def main():
    print("=== STARTING OMEGA ULTRA FORENSIC AUDIT ===")
    file_inv, ext_counts, cat_counts = scan_filesystem()
    dbs = inspect_databases()
    csvs = inspect_csvs()
    git = inspect_git()
    logs = inspect_logs()
    
    audit_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_files": len(file_inv),
        "extension_counts": ext_counts,
        "category_counts": cat_counts,
        "files": file_inv,
        "databases": dbs,
        "csv_files": csvs,
        "git": git,
        "logs": logs
    }
    
    out_json = os.path.join(OUTPUT_DIR, "raw_forensic_data.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(audit_data, f, indent=2)
        
    print(f"=== FORENSIC SCAN COMPLETE. Total Files: {len(file_inv)} | DBs: {len(dbs)} | CSVs: {len(csvs)} ===")
    print(f"Saved raw forensic data to: {out_json}")

if __name__ == "__main__":
    main()
