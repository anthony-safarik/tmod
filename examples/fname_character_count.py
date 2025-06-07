import os
from collections import defaultdict

def group_jpegs_by_name_length(root_folder):
    groups = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                name_only = os.path.splitext(filename)[0]
                name_length = len(name_only)
                full_path = os.path.join(dirpath, filename)
                groups[name_length].append(full_path)

    return groups

def report_groups(groups):
    print("JPEG File Name Length Grouping Report\n")
    for length in sorted(groups):
        count = len(groups[length])
        example = os.path.basename(groups[length][0])
        print(f"Length {length}: {count} file(s), e.g., {example}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Group JPEG files by filename length.")
    parser.add_argument("folder", help="Root folder to search")
    args = parser.parse_args()

    grouped_files = group_jpegs_by_name_length(args.folder)
    report_groups(grouped_files)
