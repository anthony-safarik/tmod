import os
import shutil
import argparse

# Define the video file extensions to look for
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.mpeg','.m4v','.mpg','.m4a','.asf','.webm'}

def remove_empty_folders_and_ds_store(directory):
    """Recursively removes all .DS_Store files and empty folders/subfolders within the given directory."""
    for root, dirs, files in os.walk(directory, topdown=False):
        # Remove .DS_Store files
        for file_name in files:
            if file_name == '.DS_Store' or file_name == 'Thumbs.db' or file_name == '.picasa.ini':
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Removed .DS_Store file: {file_path}")
                except Exception as e:
                    print(f"Failed to remove {file_path}: {e}")

        # Remove empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Now this check is more accurate post .DS_Store removal
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty folder: {dir_path}")
                except Exception as e:
                    print(f"Failed to remove {dir_path}: {e}")

def is_video_file(filename):
    return os.path.splitext(filename)[1].lower() in VIDEO_EXTENSIONS

def move_videos_preserve_structure(src_dir, tgt_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if is_video_file(file):
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_file_path, src_dir)
                tgt_file_path = os.path.join(tgt_dir, relative_path)

                if not os.path.exists(tgt_file_path):
                    os.makedirs(os.path.dirname(tgt_file_path), exist_ok=True)
                    # shutil.copy2(src_file_path, tgt_file_path)
                    os.rename(src_file_path, tgt_file_path)
                    print(f"Copied: {relative_path}")
                else:
                    print(f"Skipped (already exists): {relative_path}")

def main():
    parser = argparse.ArgumentParser(description='Move video files from one directory to another, preserving structure.')
    parser.add_argument('source', help='Source directory path')
    parser.add_argument('target', help='Target directory path')


    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        return

    os.makedirs(args.target, exist_ok=True)

    move_videos_preserve_structure(args.source, args.target)
    remove_empty_folders_and_ds_store(args.source)


if __name__ == '__main__':
    main()
