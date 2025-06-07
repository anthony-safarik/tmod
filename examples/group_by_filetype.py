# 8 character name report

import os
from collections import defaultdict

def group_by_ext(root_folder):
    groups = defaultdict(list)

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            # name_only = os.path.splitext(filename)[0]
            extension_only = os.path.splitext(filename)[1]
            # name_length = len(name_only)
            full_path = os.path.join(dirpath, filename)
            groups[extension_only].append(full_path)

    return groups

# def report_groups(groups):
#     print("File Name EXTENSION Grouping Report\n")
#     for extension in sorted(groups):
#         count = len(groups[extension])
#         example = os.path.basename(groups[extension][0])
#         print(f"extension {extension}: {count} file(s), e.g., {example}")

def report_groups(groups):
    print("File Name EXTENSION Grouping Report\n")
    # Sort by number of files per extension, descending
    sorted_groups = sorted(groups.items(), key=lambda item: len(item[1]), reverse=True)
    
    for extension, files in sorted_groups:
        count = len(files)
        example = os.path.basename(files[0])
        print(f"extension {extension}: {count} file(s), e.g., {example}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Group JPEG files by filename length.")
    parser.add_argument("folder", help="Root folder to search")
    args = parser.parse_args()

    grouped_files = group_by_ext(args.folder)
    report_groups(grouped_files)