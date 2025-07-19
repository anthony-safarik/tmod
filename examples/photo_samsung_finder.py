import os
import re
from datetime import datetime

# Allowed photo and video extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.mkv'}

def extract_date_from_folder(path):
    """Extract YYYY-MM-DD from a folder path like /2018/2018-06-22/"""
    parts = path.split(os.sep)
    if len(parts) >= 2:
        try:
            folder_date = parts[-1]
            # Validate folder_date format YYYY-MM-DD
            datetime.strptime(folder_date, '%Y-%m-%d')
            return folder_date.replace('-', '')  # Convert to YYYYMMDD
        except ValueError:
            pass
    return None

def find_matching_files(root_dir):
    matches = []

    for dirpath, _, filenames in os.walk(root_dir):
        folder_date_str = extract_date_from_folder(dirpath)
        if not folder_date_str:
            continue

        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext.lower() in ALLOWED_EXTENSIONS:
                if folder_date_str in filename:
                    full_path = os.path.join(dirpath, filename)
                    matches.append(full_path)
                    print(f"Match found: {full_path}")

    return matches

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search for photos/videos with matching date filenames.")
    parser.add_argument("root_dir", help="Root directory to search in.")
    args = parser.parse_args()

    results = find_matching_files(args.root_dir)
    print(f"\nTotal matches found: {len(results)}")
