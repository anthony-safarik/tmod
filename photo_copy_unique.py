import csv
import os
import shutil
from collections import defaultdict
import logging

# Setup logging
logging.basicConfig(
    filename='file_copy.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define source CSV and destination directory
csv_file = '/Users/tonysafarik/Git/tmod/photo_metadata_-Volumes-ORICO.csv'
destination_dir = '/Volumes/ShotVault/TEST'
log_csv = 'photo_copy_log.csv'
# csv_file = 'files.csv'
# destination_dir = 'copied_files'
# log_csv = 'copy_log.csv'

# Create destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Track seen md5 hashes and counters for naming
seen_md5 = set()
name_counters = defaultdict(int)

# Prepare log CSV
with open(log_csv, 'w', newline='', encoding='utf-8') as log_f:
    log_writer = csv.writer(log_f)
    log_writer.writerow(['original_file_path', 'date_taken', 'resolution', 'md5', 'file_size', 'new_file_path'])

    # Read source CSV and process each row
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file_path = row['file_path']
            md5_hash = row['md5']
            date_taken = row['date_taken']
            resolution = row['resolution']
            file_size = row['file_size']

            # Skip if md5 already seen
            if md5_hash in seen_md5:
                logging.info(f"Skipped duplicate MD5: {md5_hash} from {file_path}")
                continue

            # Extract year from date_taken (assumes format YYYY-MM-DD)
            year = date_taken[:4]

            # Increment counter for this year-resolution combo
            key = f"{year}_{resolution}"
            name_counters[key] += 1
            count_str = f"{name_counters[key]:06d}"

            # Build new filename
            ext = os.path.splitext(file_path)[1] or '.jpg'
            new_filename = f"{key}_{count_str}{ext}"
            destination_path = os.path.join(destination_dir, new_filename)

            # Copy file if it exists
            if os.path.isfile(file_path):
                try:
                    shutil.copy(file_path, destination_path)
                    seen_md5.add(md5_hash)
                    log_writer.writerow([file_path, date_taken, resolution, md5_hash, file_size, destination_path])
                    logging.info(f"Copied: {file_path} → {destination_path}")
                except Exception as e:
                    logging.error(f"Error copying {file_path}: {e}")
            else:
                logging.warning(f"File not found: {file_path}")
