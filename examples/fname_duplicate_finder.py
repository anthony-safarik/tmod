import os
from collections import defaultdict

def group_files_by_name(root_dir):
    file_groups = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_groups[filename].append(full_path)

    return file_groups

def report_duplicates(file_groups):
    print("Duplicate File Name Report:")
    duplicates_found = False

    for filename, paths in file_groups.items():
        if len(paths) > 1:
            duplicates_found = True
            print(f"\n'{filename}' appears {len(paths)} times:")
            for path in paths:
                print(f"  - {path}")

    if not duplicates_found:
        print("No duplicate file names found.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Group files by name and report duplicates.")
    parser.add_argument("directory", help="Directory to scan")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Please provide a valid directory.")
    else:
        file_groups = group_files_by_name(args.directory)
        report_duplicates(file_groups)
