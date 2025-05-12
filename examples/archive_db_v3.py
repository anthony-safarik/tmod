"""
Breakdown of the Script:
Database Creation (create_db):

The create_db function sets up the SQLite database and creates a table called file_data. This table stores the file path, size in bytes, MD5 hash, and timestamp.

We use INSERT OR IGNORE to prevent inserting duplicate entries based on the file path or MD5 hash.

Inserting Data into the Database (insert_file_data):

The insert_file_data function inserts file data into the database. The INSERT OR IGNORE statement ensures that if a file already exists (based on the MD5 or file path), it won’t be inserted again.

Computing MD5 Hash (compute_md5):

This function computes the MD5 hash of a given file by reading it in chunks to avoid memory issues with large files.

Loading Data from CSVs (load_csv_and_insert):

The load_csv_and_insert function reads the CSV files, extracts the relevant data, and inserts it into the database using the insert_file_data function.

Checking for Duplicates (check_duplicate):

For each file you want to check, the check_duplicate function computes its MD5 hash and queries the database to see if that hash already exists. If it does, it prints the matching file details.

Example Usage:

The script first creates the database and then loads the CSVs specified in csv_files. It then checks each file in files_to_check for duplicates in the database.

Performance Benefits:
Efficient Lookup: Searching for duplicates using an MD5 hash is very fast in a database since it's indexed and uses efficient querying methods.

Incremental Data Insertion: New CSV data can be added to the database without reloading the entire dataset into memory.

Scalability: SQLite can handle relatively large datasets, and you can scale it by moving to more robust databases like PostgreSQL or MySQL if needed.
"""

import sqlite3
import hashlib
import os
import csv

# Database setup
def create_db(db_name='file_data.db'):
    """Create a SQLite database to store file data."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE,
            bytes INTEGER,
            md5 TEXT UNIQUE,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_file_data(db_name, file_data):
    """Insert new file data into the database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Insert file data into the table, if it doesn't already exist
    cursor.execute('''
        INSERT OR IGNORE INTO file_data (file_path, bytes, md5, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (file_data['File Path'], file_data['Bytes'], file_data['MD5'], file_data['Timestamp']))
    
    conn.commit()
    conn.close()

def compute_md5(file_path):
    """Compute the MD5 hash of a file."""
    md5_hash = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def load_csv_and_insert(db_name, csv_filename):
    """Load a CSV file and insert its data into the database."""
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            file_data = {
                'File Path': row['File Path'],
                'Bytes': int(row['Bytes']),
                'MD5': row['MD5'],
                'Timestamp': row['Timestamp']
            }
            insert_file_data(db_name, file_data)

def check_duplicate(db_name, file_to_check):
    """Check if a file is a duplicate by checking its MD5 hash in the database."""
    file_md5 = compute_md5(file_to_check)
    
    if file_md5 is None:
        print(f"Skipping {file_to_check} due to error (file not found).")
        return False
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Query the database to check if the MD5 hash already exists
    cursor.execute('''
        SELECT file_path, md5, timestamp
        FROM file_data
        WHERE md5 = ?
    ''', (file_md5,))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"Duplicate found for {file_to_check}:")
        print(f"  Matching file: {result[0]}")
        print(f"  MD5: {result[1]}")
        print(f"  Timestamp: {result[2]}")
        return True
    else:
        print(f"No duplicate found for {file_to_check}.")
        return False

# Example usage
def main():
    db_name = 'file_data.db'  # Database file name
    create_db(db_name)  # Initialize the database
    
    csv_files = ['files_part1.csv', 'files_part2.csv', 'files_part3.csv']  # List of CSVs to load
    files_to_check = [
        'PHOTOS/2017/2017-05-13/DSC03570.dng',
        'PHOTOS/2017/2017-05-13/DSC03571.dng',
        'PHOTOS/2017/2017-05-13/DSC03571.JPG',
        'PHOTOS/2017/2017-05-13/DSC03572.dng'
    ]
    
    # Load CSV data into the database
    for csv_file in csv_files:
        load_csv_and_insert(db_name, csv_file)
    
    # Check for duplicates for each file
    for file in files_to_check:
        check_duplicate(db_name, file)

if __name__ == '__main__':
    main()
