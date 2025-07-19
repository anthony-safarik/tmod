import os
import argparse
from datetime import datetime

# Allowed photo and video extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi', '.mkv'}

def find_samsung_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            # if name.startswith("Y") and len(name) == 8:
            if name.startswith("image-20" or name.startswith('video-20')):
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                # print(f"Match: {full_path}")
    return matches

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

def main():
    parser = argparse.ArgumentParser(description="Find files that start with 'image-' ")
    parser.add_argument("directory", help="Directory to search")
    parser.add_argument("target", help="Path to the target directory")
    args = parser.parse_args()

    # matches = find_samsung_files(args.directory)
    matches = find_matching_files(args.directory)

    for match in matches:
        # Compute relative path from src root
        rel_path = os.path.relpath(match, args.directory)
        target_path = os.path.join(args.target, rel_path)
        print(f"Moving: {match} → {target_path}")

        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)
        os.rename(match, target_path)
        

if __name__ == "__main__":
    main()