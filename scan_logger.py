import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'scan_history.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                path TEXT,
                filename TEXT,
                extension TEXT,
                size INTEGER,
                modified TEXT,
                hash TEXT
            )
        ''')
        conn.commit()

def log_scan(df):
    if df.empty:
        return
    timestamp = datetime.now().isoformat(timespec='seconds')
    with sqlite3.connect(DB_PATH) as conn:
        rows = [
            (
                timestamp,
                row.get('Path', ''),
                row.get('Name', ''),
                row.get('Extension', ''),
                int(row.get('Size', 0)),
                row.get('Modified', ''),
                row.get('Hash', '')
            ) for _, row in df.iterrows()
        ]
        conn.executemany('''
            INSERT INTO scans (timestamp, path, filename, extension, size, modified, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', rows)
        conn.commit()
