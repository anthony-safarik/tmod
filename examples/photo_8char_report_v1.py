# write a python script that recurses a directory and reports files that match the following conditions:
# - file extension is one of ['.jpg', '.arw', '.dng', '.mp4', '.mov','.avi'] (case insensitive)
# - file name length is 8 characters

import os
import datetime

# Allowed extensions (lowercase for case-insensitive comparison)
VALID_EXTENSIONS = {'.jpg', '.arw', '.dng', '.mp4', '.mov', '.avi'}
# VALID_EXTENSIONS = {'.mp4', '.mov', '.avi'}

def is_valid_file(file_name):
    base_name, ext = os.path.splitext(file_name)
    return len(base_name) == 8 and ext.lower() in VALID_EXTENSIONS

def get_creation_date(path):
    try:
        stat = os.stat(path)
        # On Windows, st_ctime is creation time
        # On Unix, st_ctime is last metadata change; use st_birthtime if available
        if hasattr(stat, 'st_birthtime'):
            return datetime.datetime.fromtimestamp(stat.st_birthtime)
        else:
            return datetime.datetime.fromtimestamp(stat.st_ctime)
    except Exception as e:
        return f"Error retrieving date: {e}"

# def find_matching_files(root_dir):
#     matching_files = []
#     for dirpath, _, filenames in os.walk(root_dir):
#         for fname in filenames:
#             if is_valid_file(fname):
#                 full_path = os.path.join(dirpath, fname)
#                 creation_date = get_creation_date(full_path)
#                 matching_files.append((full_path, creation_date))
#     return matching_files

# def find_matching_files(root_dir):
#     matching_files = []
#     for dirpath, _, filenames in os.walk(root_dir):
#         for fname in filenames:
#             if is_valid_file(fname):
#                 full_path = os.path.join(dirpath, fname)
#                 creation_date = get_creation_date(full_path)
#                 if isinstance(creation_date, datetime.datetime):
#                     creation_date_str = creation_date.strftime("%Y-%m-%d")
#                 else:
#                     creation_date_str = str(creation_date)
#                 matching_files.append((full_path, creation_date_str))
#     return matching_files

def find_matching_files(root_dir):
    matching_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if is_valid_file(fname):
                full_path = os.path.join(dirpath, fname)
                creation_date = get_creation_date(full_path)
                if isinstance(creation_date, datetime.datetime):
                    creation_date_str = creation_date.strftime("%Y-%m-%d")
                else:
                    creation_date_str = str(creation_date)
                matching_files.append((full_path, creation_date, creation_date_str == os.path.basename(dirpath)))
    return matching_files

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find files with 8-character names and specific extensions.")
    parser.add_argument("directory", help="Root directory to scan")

    args = parser.parse_args()
    results = find_matching_files(args.directory)

    print("Matching files:")
    for file_path, creation_date, match in results:
        print(f"{file_path} | Created: {creation_date} - {match}")

