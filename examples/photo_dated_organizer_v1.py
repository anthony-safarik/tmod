#renames 8 char files with date prefix

import os
import argparse

VALID_EXTENSIONS = {'.jpg', '.arw', '.dng', '.mp4', '.mov', '.avi'}

def find_dsc_files(directory):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if len(name) == 8 and ext.lower() in VALID_EXTENSIONS:
                full_path = os.path.join(root, filename)
                matches.append(full_path)
                # print(f"Match: {full_path}")
    return matches


def get_date_renamed_file_path(file_path):
    fp_dir = os.path.dirname(file_path)
    fp_basename = os.path.basename(file_path)
    fp_parent = os.path.basename(fp_dir)
    if len(fp_parent) >= 10:
        date_string = fp_parent[:10].replace('-','') + '-'
        renamed_path = os.path.join(fp_dir, date_string + fp_basename)
        return renamed_path   

def main():
    parser = argparse.ArgumentParser(description="Find files that are 8 characters and rename based on dated folder.")
    parser.add_argument("directory", help="Directory to search")
    parser.add_argument("target", help="Path to the target directory")
    args = parser.parse_args()

    matches = find_dsc_files(args.directory)

    for match in matches:
        # Compute relative path from src root
        rel_path = os.path.relpath(match, args.directory)


        target_path = os.path.join(args.target, rel_path)
        renamed_target_path = get_date_renamed_file_path(target_path)

        if renamed_target_path:
            print(rel_path, renamed_target_path)

            target_dir = os.path.dirname(renamed_target_path)
            os.makedirs(target_dir, exist_ok=True)
            os.rename(match, renamed_target_path)
        

if __name__ == "__main__":
    main()