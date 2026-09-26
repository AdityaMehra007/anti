import sqlite3, os
db_dir = os.path.expanduser('~/AppData/Local/hermes')
for name in ['state.db', 'kanban.db', 'verification_evidence.db']:
    path = os.path.join(db_dir, name)
    conn = sqlite3.connect(path)
    result = conn.execute('PRAGMA integrity_check').fetchone()
    print(f'{name}: {result}')
    conn.close()