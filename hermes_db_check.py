import sqlite3

db_paths = [
    r'C:\Users\amehr\AppData\Local\hermes\state.db',
    r'C:\Users\amehr\AppData\Local\hermes\kanban.db',
    r'C:\Users\amehr\AppData\Local\hermes\verification_evidence.db',
]

for path in db_paths:
    try:
        conn = sqlite3.connect(path)
        result = conn.execute('PRAGMA integrity_check').fetchone()
        status = result[0]
        print(f'{path}: {status}')
        conn.close()
    except Exception as e:
        print(f'{path}: ERROR - {e}')