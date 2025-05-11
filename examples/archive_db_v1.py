"""
creates and adds file info to sqlite db
"""

import os
import hashlib
import sqlite3
import shutil

DB_FILE = "archive.db"
ARCHIVE_DIR = "archive"
DUPLICATE_DIR = "duplicates"

def get_md5(file_path):
    """Compute the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_path TEXT,
            md5_hash TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def file_exists(md5_hash):
    """Check if a file with the same MD5 hash exists in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM files WHERE md5_hash = ?", (md5_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_file_to_db(file_name, file_path, md5_hash):
    """Add a new file record to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_name, file_path, md5_hash) VALUES (?, ?, ?)",
                   (file_name, file_path, md5_hash))
    conn.commit()
    conn.close()

def process_folder(folder_path):
    """Process new files in a folder, segregating duplicates."""
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            md5_hash = get_md5(file_path)

            if file_exists(md5_hash):
                print(f"Duplicate found: {file_name}. Moving to {DUPLICATE_DIR}.")
                shutil.move(file_path, os.path.join(DUPLICATE_DIR, file_name))
            else:
                new_archive_path = os.path.join(ARCHIVE_DIR, file_name)
                shutil.move(file_path, new_archive_path)
                add_file_to_db(file_name, new_archive_path, md5_hash)
                print(f"Archived: {file_name}")

if __name__ == "__main__":
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(DUPLICATE_DIR, exist_ok=True)
    init_db()
    
    folder_to_process = input("Enter the path of the folder to archive: ").strip()
    if os.path.exists(folder_to_process):
        process_folder(folder_to_process)
    else:
        print("Invalid folder path.")
