import os
import shutil
import datetime
from pathlib import Path

# Define common video file extensions
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm'}
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.arw', '.dng'}

def is_video_file(filename):
    return Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS

def move_and_organize_videos(src_directory, dest_directory):
    for root, _, files in os.walk(src_directory):
        for filename in files:
            if is_video_file(filename):
                original_path = os.path.join(root, filename)
                # Get file's modification date
                mod_time = os.path.getmtime(original_path)
                mod_date = datetime.datetime.fromtimestamp(mod_time)
                yyyy = mod_date.strftime("%Y")
                yyyy_mm_dd = mod_date.strftime("%Y-%m-%d")
                yyyymmdd = mod_date.strftime("%Y%m%d")

                # Create destination path
                dest_subfolder = os.path.join(dest_directory, yyyy, yyyy_mm_dd)
                os.makedirs(dest_subfolder, exist_ok=True)

                # Rename the file
                new_filename = f"{yyyymmdd}-{filename}"
                new_path = os.path.join(dest_subfolder, new_filename)

                # Avoid overwriting
                if os.path.exists(new_path):
                    print(f"Skipped (target exists): {new_path}")
                    continue

                print(f"Moving: {original_path} → {new_path}")
                shutil.move(original_path, new_path)

if __name__ == "__main__":
    src = input("Enter the source directory to search: ").strip()
    dest = input("Enter the destination directory to organize into: ").strip()

    if os.path.isdir(src) and os.path.isdir(dest):
        move_and_organize_videos(src, dest)
    else:
        print("One or both directories are invalid.")
