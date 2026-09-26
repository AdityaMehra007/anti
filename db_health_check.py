import sqlite3, os, sys

results = []
hermes_db_dir = r'C:\Users\amehr\AppData\Local\hermes'
e_anti_dbs = []

# Check e:\anti databases
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join('/e/anti', name)
    if os.path.exists(path):
        e_anti_dbs.append((name, path))

# Check hermes databases
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join(hermes_db_dir, name)
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            result = conn.execute('PRAGMA integrity_check').fetchone()
            status = result[0]
            conn.close()
            results.append(f'{name} (hermes): {status}')
        except Exception as e:
            results.append(f'{name} (hermes): ERROR - {e}')

# Report
for r in results:
    print(r)

print()
if e_anti_dbs:
    for name, path in e_anti_dbs:
        size = os.path.getsize(path)
        print(f'e:\\anti\\{name}: exists, size={size} bytes')
else:
    print('No hermes-mapped databases found in /e/anti')