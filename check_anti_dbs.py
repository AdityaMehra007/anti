import sqlite3, os

# Check e:\anti databases
db_dir = '/e/anti'
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join(db_dir, name)
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            result = conn.execute('PRAGMA integrity_check').fetchone()
            status = result[0]
            size = os.path.getsize(path)
            print(f'e:\\anti\\{name}: exists, size={size} bytes, integrity: {status}')
            conn.close()
        except Exception as e:
            print(f'e:\\anti\\{name}: ERROR - {e}')
    else:
        print(f'e:\\anti\\{name}: NOT FOUND')