import os
import glob
import sqlite3
import json
import csv

def inspect_databases():
    print("==================================================")
    print("             SQLITE DATABASE AUDIT                ")
    print("==================================================")
    db_files = glob.glob('e:/anti/**/*.db', recursive=True) + glob.glob('e:/anti/**/*.sqlite', recursive=True)
    summary = {}
    for db_path in sorted(db_files):
        # normalize path
        norm_path = db_path.replace('\\', '/')
        if 'node_modules' in norm_path or '.git' in norm_path:
            continue
        size = os.path.getsize(db_path)
        print(f"\n[DB] {norm_path} ({size:,} bytes)")
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
            summary[norm_path] = {"size": size, "tables": {}}
            for t in tables:
                try:
                    cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                    summary[norm_path]["tables"][t] = cnt
                    print(f"  - {t}: {cnt} rows")
                except Exception as e:
                    print(f"  - {t}: error ({e})")
            conn.close()
        except Exception as e:
            print(f"  ERROR opening: {e}")
    return summary

def inspect_csvs():
    print("\n==================================================")
    print("                 CSV DATASET AUDIT                ")
    print("==================================================")
    csv_files = glob.glob('e:/anti/**/*.csv', recursive=True)
    summary = {}
    for p in sorted(csv_files):
        norm_path = p.replace('\\', '/')
        if 'node_modules' in norm_path or '.git' in norm_path:
            continue
        size = os.path.getsize(p)
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                rows = sum(1 for _ in reader)
            summary[norm_path] = {"size": size, "rows": rows, "header": header}
            print(f"[CSV] {norm_path} | {rows:,} data rows | Columns: {len(header) if header else 0}")
            if header:
                print(f"      Headers: {', '.join(header[:6])}...")
        except Exception as e:
            print(f"[CSV] {norm_path} | Error: {e}")
    return summary

def inspect_subsystems():
    print("\n==================================================")
    print("               SUBSYSTEM DIRECTORIES              ")
    print("==================================================")
    dirs = [d for d in os.listdir('e:/anti') if os.path.isdir(os.path.join('e:/anti', d))]
    for d in sorted(dirs):
        full_dir = os.path.join('e:/anti', d)
        file_count = sum(len(files) for _, _, files in os.walk(full_dir))
        size = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(full_dir) for f in files if os.path.exists(os.path.join(r, f)))
        print(f"Directory: {d.padEnd(30) if hasattr(d, 'padEnd') else d:<30} | {file_count:>5} files | {size:>12,} bytes")

if __name__ == '__main__':
    inspect_databases()
    inspect_csvs()
    inspect_subsystems()
