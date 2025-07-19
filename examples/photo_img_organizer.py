import os
import shutil
import re
import argparse
from pathlib import Path

def organize_img_files(source_dir, target_root):
    # Regex pattern to match filenames like IMG_20200605_130606.jpg
    pattern = re.compile(r'^IMG_(\d{4})(\d{2})(\d{2})_.*\.(jpg|jpeg|png|mp4)$', re.IGNORECASE)

    for root, _, files in os.walk(source_dir):
        for filename in files:
            match = pattern.match(filename)
            if match:
                year, month, day = match.groups()[:3]
                date_folder = f"{year}/{year}-{month}-{day}"

                # Create target directory path
                target_dir = os.path.join(target_root, date_folder)
                os.makedirs(target_dir, exist_ok=True)

                # Full source and target paths
                src_path = os.path.join(root, filename)
                dst_path = os.path.join(target_dir, filename)

                if not os.path.exists(dst_path):
                    print(f"Moving: {src_path} → {dst_path}")
                    shutil.move(src_path, dst_path)
                else:
                    print(f"Skipping (already exists): {dst_path}")

    delete_empty_dirs(source_dir)

def delete_empty_dirs(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if dirpath == root_dir:
            continue
        if not dirnames and not filenames:
            print(f"Removing empty folder: {dirpath}")
            os.rmdir(dirpath)

def main():
    parser = argparse.ArgumentParser(description="Organize IMG files into date-based folders.")
    parser.add_argument("source", help="Path to the source directory")
    parser.add_argument("target", help="Path to the target directory")
    args = parser.parse_args()

    organize_img_files(args.source, args.target)

if __name__ == "__main__":
    main()
