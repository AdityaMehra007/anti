import sqlite3
import csv
import os

print("="*80)
print("ANALYZING PEOPLE FROM ACCENTURE IN CAREER INTELLIGENCE DB")
print("="*80)

db_path = os.path.join("data", "aditya_global_career_intelligence.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get column names of people
cur.execute("PRAGMA table_info(people)")
col_info = cur.fetchall()
cols = [c[1] for c in col_info]
print("Columns in people table:", cols)

cur.execute("SELECT * FROM people WHERE LOWER(company_name) LIKE '%accenture%'")
rows = cur.fetchall()
print(f"Total matching rows in 'people' table: {len(rows)}")
for i, r in enumerate(rows[:5], 1):
    d = dict(zip(cols, r))
    print(f"Row {i}:", {k: v for k, v in d.items() if v is not None and v != ''})


roles_count = {}
departments_count = {}
locations_count = {}

people_list = []
for r in rows:
    p = dict(zip(cols, r))
    people_list.append(p)
    role = p.get('role') or p.get('designation') or p.get('title') or 'Unknown'
    dept = p.get('department') or 'General'
    loc = p.get('location') or 'Bengaluru'
    roles_count[role] = roles_count.get(role, 0) + 1
    departments_count[dept] = departments_count.get(dept, 0) + 1
    locations_count[loc] = locations_count.get(loc, 0) + 1

print("\n--- Top Roles ---")
for r, c in sorted(roles_count.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {r}: {c}")

print("\n--- Departments ---")
for d, c in sorted(departments_count.items(), key=lambda x: x[1], reverse=True):
    print(f"  {d}: {c}")

print("\n--- First 20 People ---")
for i, p in enumerate(people_list[:20], 1):
    name = p.get('full_name') or p.get('name') or p.get('first_name', '') + ' ' + p.get('last_name', '')
    role = p.get('role') or p.get('designation') or p.get('title') or ''
    email = p.get('email') or p.get('corporate_email') or p.get('business_email') or ''
    phone = p.get('public_business_phone') or p.get('phone') or ''
    li = p.get('linkedin_url') or p.get('linkedin') or ''
    print(f"{i:2d}. {name} | Role: {role} | Email: {email} | Phone: {phone} | LI: {li}")

print("\n" + "="*80)
print("CHECKING ALL OTHER CSV AND SQLITE DATABASES FOR ADDITIONAL ACCENTURE CONTACTS")
print("="*80)

# Check Recruiter_and_Hiring_Contacts_Master_Database.csv
rec_csv = os.path.join("data", "Recruiter_and_Hiring_Contacts_Master_Database.csv")
if os.path.exists(rec_csv):
    with open(rec_csv, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        accenture_in_rec = [row for row in reader if any("accenture" in str(v).lower() for v in row.values())]
        print(f"Recruiter_and_Hiring_Contacts_Master_Database.csv: {len(accenture_in_rec)} rows")

# Check outreach_tracker.db
ot_db = os.path.join("data", "outreach_tracker.db")
if os.path.exists(ot_db):
    try:
        conn_ot = sqlite3.connect(ot_db)
        cur_ot = conn_ot.cursor()
        cur_ot.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tbls = cur_ot.fetchall()
        print(f"outreach_tracker.db tables: {tbls}")
        for (t,) in tbls:
            cur_ot.execute(f"SELECT COUNT(*) FROM {t} WHERE LOWER(company) LIKE '%accenture%'")
            print(f"  {t}: {cur_ot.fetchone()[0]} rows")
    except Exception as e:
        print(f"outreach_tracker.db error: {e}")

# Check outreach_vault_4500.sqlite
ov_db = os.path.join("data", "outreach_vault_4500.sqlite")
if os.path.exists(ov_db):
    try:
        conn_ov = sqlite3.connect(ov_db)
        cur_ov = conn_ov.cursor()
        cur_ov.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tbls = cur_ov.fetchall()
        print(f"outreach_vault_4500.sqlite tables: {tbls}")
        for (t,) in tbls:
            try:
                cur_ov.execute(f"SELECT COUNT(*) FROM {t} WHERE LOWER(company_name) LIKE '%accenture%'")
                print(f"  {t}: {cur_ov.fetchone()[0]} rows")
            except:
                pass
    except Exception as e:
        print(f"outreach_vault_4500.sqlite error: {e}")
