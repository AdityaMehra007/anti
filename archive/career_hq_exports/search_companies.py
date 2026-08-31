import sqlite3
import sys
import os

db_path = r"E:\OMNI_OS\CAREER_HQ\company_universe_100k.db"

def search(query="", industry="", bengaluru_only=False, limit=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    sql = "SELECT id, name, industry, headquarters, tier, ats_type, career_url FROM companies WHERE 1=1"
    params = []
    
    if query:
        sql += " AND name LIKE ?"
        params.append(f"%{query}%")
    if industry:
        sql += " AND industry LIKE ?"
        params.append(f"%{industry}%")
    if bengaluru_only:
        sql += " AND has_bengaluru_hub = 1"
        
    sql += f" LIMIT {limit};"
    
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    q = sys.argv[1] if len(sys.argv) > 1 else "Goldman"
    results = search(query=q, limit=5)
    print(f"--- Search Results for '{q}' ---")
    for r in results:
        print(f"[{r[0]}] {r[1]} | {r[2]} | HQ: {r[3]} | {r[4]} | ATS: {r[5]}")