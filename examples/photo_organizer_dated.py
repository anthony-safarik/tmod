import os
import re
import shutil
import argparse

def organize_files_by_date(source_dir, dest_root):
    # Regex to match filenames like 20211031-DSC07187.JPG
    date_prefix_pattern = re.compile(r'^(\d{4})(\d{2})(\d{2})')

    for root, _, files in os.walk(source_dir):
        for filename in files:
            match = date_prefix_pattern.match(filename)
            if match:
                year, month, day = match.groups()
                date_folder = f"{year}-{month}-{day}"
                
                source_path = os.path.join(root, filename)
                target_path = os.path.join(dest_root, year, date_folder)
                os.makedirs(target_path, exist_ok=True)

                dest_file_path = os.path.join(target_path, filename)

                if os.path.abspath(source_path) != os.path.abspath(dest_file_path):
                    print(f"Moving: {source_path} -> {dest_file_path}")
                    # shutil.move(source_path, dest_file_path)

def main():
    parser = argparse.ArgumentParser(
        description="Organize files into folders by date prefix (YYYYMMDD-) in filenames."
    )
    parser.add_argument("source", help="Source directory to search")
    parser.add_argument("target", help="Target root directory for sorted files")

    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: Source directory '{args.source}' does not exist.")
        return

    os.makedirs(args.target, exist_ok=True)
    organize_files_by_date(args.source, args.target)

if __name__ == "__main__":
    main()
