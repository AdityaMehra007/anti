import sqlite3
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

conn = sqlite3.connect(r"e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite")
cur = conn.cursor()

if len(sys.argv) > 1 and sys.argv[1].strip().upper().startswith("SELECT"):
    sql = sys.argv[1]
    # Handle common column aliases if querying master_search_fts directly
    if "master_search_fts" in sql.lower():
        sql = re.sub(r"\bcompany_name\b", "entity_name", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bhr_lead\b", "contact_name", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bhr_email\b", "email", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\blocation\b", "corridor", sql, flags=re.IGNORECASE)
    
    # Handle aliases for tech_parks
    if "tech_parks" in sql.lower():
        sql = re.sub(r"\blocation_corridor\b", "corridor", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bmicro_market\b", "corridor", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bcompany_count\b", "transit_friction_index", sql, flags=re.IGNORECASE)

    # Handle aliases for top_employers
    if "top_employers" in sql.lower():
        sql = re.sub(r"\bindustry_tier\b", "category", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\blocation_hub\b", "location", sql, flags=re.IGNORECASE)
        sql = re.sub(r"\bsalary_range\b", "total_ctc_lpa", sql, flags=re.IGNORECASE)
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        print(" | ".join(str(x) for x in r))
else:
    raw_term = sys.argv[1] if len(sys.argv) > 1 else 'Founder OR "Chief of Staff"'
    # Convert single quotes to double quotes for SQLite FTS5 syntax
    match_term = re.sub(r"'(.*?)'", r'"\1"', raw_term)
    
    sql = """
    SELECT entity_name, contact_name, email, phone, corridor 
    FROM master_search_fts 
    WHERE master_search_fts MATCH ? 
    LIMIT 15
    """
    cur.execute(sql, (match_term,))
    rows = cur.fetchall()
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
