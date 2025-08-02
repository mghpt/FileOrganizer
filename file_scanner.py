import os
import pandas as pd
import hashlib
import sqlite3
from datetime import datetime

def log_scan_to_db(record_count):
    db_path = os.path.join('download', 'scan_history.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            file_count INTEGER
        )
    ''')
    cursor.execute('INSERT INTO scan_history (timestamp, file_count) VALUES (?, ?)',
                   (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), record_count))
    conn.commit()
    conn.close()

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def hash_file(path, block_size=65536):
    try:
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def scan_drive(drive_path='D:\\'):
    records = []
    for root, _, files in os.walk(drive_path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                mtime = os.path.getmtime(filepath)
                mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
                records.append({
                    'Path': filepath,
                    'Size': format_size(size),
                    'Modified': mtime_str
                })
            except Exception:
                continue

    log_scan_to_db(len(records))
    return pd.DataFrame(records)

def find_duplicates(drive_path='D:\\'):
    file_hashes = {}
    duplicates = []

    for root, _, files in os.walk(drive_path):
        for file in files:
            path = os.path.join(root, file)
            try:
                h = hash_file(path)
                if not h:
                    continue
                if h in file_hashes:
                    if not any(d['Path'] == file_hashes[h] for d in duplicates):
                        duplicates.append({
                            'Hash': h,
                            'Path': file_hashes[h],
                            'Size': format_size(os.path.getsize(file_hashes[h]))
                        })
                    duplicates.append({
                        'Hash': h,
                        'Path': path,
                        'Size': format_size(os.path.getsize(path))
                    })
                else:
                    file_hashes[h] = path
            except Exception:
                continue

    return pd.DataFrame(duplicates)
