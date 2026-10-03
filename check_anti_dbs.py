import sqlite3, os

results = []

# Check e:\anti databases
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join('/e/anti', name)
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            result = conn.execute('PRAGMA integrity_check').fetchone()
            status = result[0]
            conn.close()
            results.append(f'{name}: {status}')
        except Exception as e:
            results.append(f'{name}: ERROR - {e}')
    else:
        results.append(f'{name}: NOT FOUND')

for r in results:
    print(r)