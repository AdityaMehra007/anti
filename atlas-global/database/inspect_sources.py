import sqlite3

def check_db(path, label):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    print(f"=== {label} ===")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [r[0] for r in cur.fetchall()]
    for t in tables:
        try:
            cnt = cur.execute(f"SELECT count(1) FROM {t}").fetchone()[0]
            print(f"  {t}: {cnt}")
        except Exception as e:
            print(f"  {t}: {e}")
    conn.close()

check_db(r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite", "Apex DB")
check_db(r"e:\anti\data\aditya_global_career_intelligence.db", "Career Intelligence DB")
