import os
import shutil
import re
import argparse

# Photo and video file extensions (case-insensitive check)
PHOTO_VIDEO_EXTENSIONS = {
    '.jpg', '.arw', '.jpeg', '.mp4', '.avi', '.m4v', '.mpg',
    '.gif', '.mov', '.dng', '.psd', '.bdm', '.asf', '.ind',
    '.thm', '.tif', '.png'
}

def move_media_with_date_prefix(source_dir, target_dir):
    date_folder_pattern = re.compile(r'(\d{4})[/-](\d{2})[/-](\d{2})')

    for root, _, files in os.walk(source_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in PHOTO_VIDEO_EXTENSIONS:
                continue  # Skip unsupported file types

            source_path = os.path.join(root, file)

            # Find YYYY-MM-DD in the path components
            parts = os.path.normpath(source_path).split(os.sep)
            date_str = None
            for part in parts:
                match = date_folder_pattern.match(part)
                if match:
                    date_str = f"{match.group(1)}{match.group(2)}{match.group(3)}"
                    year = match.group(1)
                    break

            if not date_str:
                print(f"Skipping {source_path} - no date folder found in path")
                continue

            # Build the destination path
            new_filename = f"{date_str}-{file}"
            target_subdir = os.path.join(target_dir, year, f"{year}-{date_str[4:6]}-{date_str[6:]}")
            # os.makedirs(target_subdir, exist_ok=True)
            target_path = os.path.join(target_subdir, new_filename)

            print(f"Moving: {source_path} -> {target_path}")
            # shutil.move(source_path, target_path)

def main():
    parser = argparse.ArgumentParser(description='Move and rename photo/video files with a date prefix.')
    parser.add_argument('source_directory', help='Path to the source directory')
    parser.add_argument('target_directory', help='Path to the target directory')
    args = parser.parse_args()

    move_media_with_date_prefix(args.source_directory, args.target_directory)

if __name__ == '__main__':
    main()
