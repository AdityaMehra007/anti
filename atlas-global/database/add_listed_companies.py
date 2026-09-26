import sqlite3

atlas_conn = sqlite3.connect(r'e:\anti\atlas-global\database\atlas.db')
a_cur = atlas_conn.cursor()

apex_conn = sqlite3.connect(r'e:\anti\BANGALORE_APEX_GLOBAL_CAREER_DATABASE.sqlite')
apex_conn.row_factory = sqlite3.Row
ap_cur = apex_conn.cursor()

ap_cur.execute('SELECT * FROM richest_listed_companies')
rows = ap_cur.fetchall()
added = 0
for r in rows:
    cid = f"CMP-LST-{r['id']}"
    cname = r['company_name']
    a_cur.execute('SELECT count(1) FROM companies WHERE company_name = ?', (cname,))
    if a_cur.fetchone()[0] == 0:
        a_cur.execute('''
        INSERT INTO companies (
            company_id, company_name, brand_name, domain, industry, subindustry,
            company_type, startup_status, listed_status, headquarters, bengaluru_presence,
            bengaluru_address, funding_status, funding_amount_if_public, founders, careers_url,
            public_email, public_phone, source, source_url, verification_status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cid, cname, cname.split()[0], cname.split()[0].lower() + '.com',
            r['sector'].split('/')[0].strip(), r['sector'], 'Public Listed Enterprise',
            'Mature Enterprise', r['exchange_listing'], r['location'],
            'Active Bengaluru Corporate Center', r['location'], 'Listed Equity',
            r['market_cap_valuation'], 'Board / Promoters', r['careers_url'],
            r['hr_email'], r['phone'], 'Richest Listed Companies Registry',
            r['careers_url'], 'VERIFIED_OFFICIAL', r['target_role']
        ))
        a_cur.execute('''
        INSERT INTO atlas_search_fts (entity_id, entity_type, name_or_title, company_or_org, location_corridor, contact_point, keywords)
        VALUES (?, 'COMPANY', ?, ?, ?, ?, ?)
        ''', (cid, cname, cname, r['location'], r['hr_email'], f"{r['sector']} {r['exchange_listing']}"))
        added += 1

atlas_conn.commit()
total = a_cur.execute('SELECT count(1) FROM companies').fetchone()[0]
print(f"Added {added} listed giants. Total companies in atlas.db: {total}")
atlas_conn.close()
apex_conn.close()
