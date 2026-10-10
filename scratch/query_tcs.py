import sqlite3

conn = sqlite3.connect('C:/Users/amehr/.gemini/antigravity/brain/2d7dcea9-02af-4ae3-93a7-88b5d217683c/bangalore_companies.db')
c = conn.cursor()

c.execute("SELECT id, name, category, sub_sector, bangalore_zone, key_address_or_park, careers_url FROM companies WHERE name LIKE '%TCS%' OR name LIKE '%Tata%'")
rows = c.fetchall()
print(f"Total matching companies: {len(rows)}")
for r in rows:
    print(r)
conn.close()
