import sqlite3, os

# Check hermes databases
hermes_db_dir = r'C:\Users\amehr\AppData\Local\hermes'
print("=== Hermes Databases ===")
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join(hermes_db_dir, name)
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            result = conn.execute('PRAGMA integrity_check').fetchone()
            status = result[0]
            size = os.path.getsize(path)
            print(f'{name}: {status} (size: {size:,} bytes)')
            conn.close()
        except Exception as e:
            print(f'{name}: ERROR - {e}')
    else:
        print(f'{name}: NOT FOUND')

print()

# Check e:\anti databases
anti_db_dir = '/e/anti'
print("=== e:\anti Databases ===")
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join(anti_db_dir, name)
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            result = conn.execute('PRAGMA integrity_check').fetchone()
            status = result[0]
            size = os.path.getsize(path)
            print(f'{name}: {status} (size: {size:,} bytes)')
            conn.close()
        except Exception as e:
            print(f'{name}: ERROR - {e}')
    else:
        print(f'{name}: NOT FOUND')