import csv
import os
import shutil
import logging

# Setup logging
logging.basicConfig(
    filename='file_copy.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

csv_file = '/Volumes/ShotVault/PHOTOS/PHOTO_META_ALL.csv'
destination_dir = '/Volumes/ShotVault/PHOTOS'
log_csv = 'photo_copy_log.csv'
# csv_file = 'files.csv'
# destination_dir = 'copied_files'
# log_csv = 'copy_log.csv'

# Create destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Track seen md5 hashes
seen_md5 = set()

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

            # Copy file if it exists
            if os.path.isfile(file_path):
                # print(file_path)
                try:
                    # Preserve subdirectory structure
                    # relative_path = os.path.relpath(file_path)
                    # relative_path = file_path
                    # destination_path = os.path.join(destination_dir, relative_path)
                    destination_path = destination_dir + file_path
                    print(destination_path)
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                    shutil.copy2(file_path, destination_path)
                    seen_md5.add(md5_hash)

                    log_writer.writerow([file_path, date_taken, resolution, md5_hash, file_size, destination_path])
                    logging.info(f"Copied: {file_path} → {destination_path}")
                except Exception as e:
                    logging.error(f"Error copying {file_path}: {e}")
            else:
                logging.warning(f"File not found: {file_path}")
