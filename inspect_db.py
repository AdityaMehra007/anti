import sqlite3

conn = sqlite3.connect("data/outreach_vault_4500.sqlite")
cursor = conn.cursor()

sectors = cursor.execute("SELECT sector, count(*) FROM outreach_ledger GROUP BY sector").fetchall()
print("Sectors:")
for s, c in sectors:
    print(f"  {s}: {c}")

print("\nTop 25 Companies:")
comps = cursor.execute("SELECT company, count(*), target_role FROM outreach_ledger GROUP BY company ORDER BY count(*) DESC LIMIT 25").fetchall()
for comp, cnt, role in comps:
    print(f"  {comp} ({cnt} contacts) - Role: {role}")

conn.close()
